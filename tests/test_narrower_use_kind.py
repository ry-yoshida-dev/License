from dataclasses import dataclass, replace
from enum import Enum

import pytest
from typing_extensions import override

from license_kit import (
    IntendedUse,
    License,
    LicenseDefinition,
    LicenseTerms,
    NarrowerUseKind,
    Permission,
    Restriction,
    UseAssessment,
    UseKind,
    find_broader_kinds,
)


class CommissionKind(Enum):
    """Commercial use narrowed by who commissions the work, as some public data terms tell them apart."""

    COMMISSIONED_WORK = "commissioned_work"
    PUBLIC_COMMISSION = "public_commission"

    @property
    def broader(self) -> UseKind | NarrowerUseKind:
        match self:
            case CommissionKind.COMMISSIONED_WORK:
                return UseKind.COMMERCIAL_USE
            case CommissionKind.PUBLIC_COMMISSION:
                return CommissionKind.COMMISSIONED_WORK


class LoopingKind(Enum):
    FIRST = "first"
    SECOND = "second"

    @property
    def broader(self) -> NarrowerUseKind:
        return LoopingKind.SECOND if self is LoopingKind.FIRST else LoopingKind.FIRST


@dataclass(frozen=True, kw_only=True)
class CommissionedUse(IntendedUse):
    is_commissioned_by_public_body: bool

    @property
    @override
    def narrower_kinds(self) -> frozenset[NarrowerUseKind]:
        return frozenset({CommissionKind.PUBLIC_COMMISSION} if self.is_commissioned_by_public_body else ())


@dataclass(frozen=True, kw_only=True)
class CommissionTerms(LicenseTerms):
    public_commission: Permission

    @property
    @override
    def stated_kinds(self) -> tuple[UseKind | NarrowerUseKind, ...]:
        return (*super().stated_kinds, CommissionKind.PUBLIC_COMMISSION)

    @override
    def permission_for(self, kind: UseKind | NarrowerUseKind) -> Permission:
        if kind is CommissionKind.PUBLIC_COMMISSION:
            return self.public_commission
        return super().permission_for(kind)


def with_public_commission(terms: LicenseTerms, permission: Permission) -> CommissionTerms:
    return CommissionTerms(
        commercial_use=terms.commercial_use,
        non_research_use=terms.non_research_use,
        ai_training=terms.ai_training,
        modification=terms.modification,
        redistribution=terms.redistribution,
        modified_redistribution=terms.modified_redistribution,
        network_service=terms.network_service,
        attribution=terms.attribution,
        modification_notice=terms.modification_notice,
        source_disclosure=terms.source_disclosure,
        downstream_terms=terms.downstream_terms,
        share_alike=terms.share_alike,
        public_commission=permission,
    )


NON_COMMERCIAL: LicenseTerms = License.CC_BY_NC_4_0.definition.terms
# Non-commercial terms that let work commissioned by a public body go ahead.
PUBLIC_WORK_TERMS: CommissionTerms = with_public_commission(NON_COMMERCIAL, Permission.ALLOWED)
PUBLIC_WORK_LICENSE: LicenseDefinition = LicenseDefinition(
    title="Non-commercial terms open to public commissions",
    short_title="Public work",
    terms=PUBLIC_WORK_TERMS,
    identifier="LicenseRef-Public-Work",
    url=None,
)


@pytest.fixture
def public_commission(private_use: IntendedUse) -> CommissionedUse:
    return CommissionedUse(
        is_commercial=True,
        is_research_only=private_use.is_research_only,
        is_used_for_ai_training=private_use.is_used_for_ai_training,
        is_modified=private_use.is_modified,
        is_combined=private_use.is_combined,
        is_redistributed=private_use.is_redistributed,
        is_offered_over_network=private_use.is_offered_over_network,
        is_commissioned_by_public_body=True,
    )


class TestNarrowerUseKind:
    def test_broader_kinds_run_from_the_nearest_to_a_use_kind(self) -> None:
        assert find_broader_kinds(CommissionKind.PUBLIC_COMMISSION) == (
            CommissionKind.COMMISSIONED_WORK,
            UseKind.COMMERCIAL_USE,
        )

    def test_cycle_of_broader_kinds_is_refused(self) -> None:
        with pytest.raises(ValueError, match="cycle"):
            _ = find_broader_kinds(LoopingKind.FIRST)

    def test_narrower_kind_stands_in_for_every_kind_it_narrows(self, public_commission: CommissionedUse) -> None:
        assert public_commission.involved_kinds == {UseKind.NON_RESEARCH_USE, CommissionKind.PUBLIC_COMMISSION}
        assert replace(public_commission, is_commissioned_by_public_body=False).involved_kinds == {
            UseKind.NON_RESEARCH_USE,
            UseKind.COMMERCIAL_USE,
        }

    def test_narrowing_a_kind_the_use_does_not_involve_is_refused(self, public_commission: CommissionedUse) -> None:
        with pytest.raises(ValueError, match="does not involve"):
            _ = replace(public_commission, is_commercial=False)

    def test_terms_unaware_of_a_narrower_kind_answer_for_the_broader_one(self) -> None:
        assert NON_COMMERCIAL.permission_for(CommissionKind.PUBLIC_COMMISSION) is Permission.PROHIBITED
        assert PUBLIC_WORK_TERMS.permission_for(CommissionKind.COMMISSIONED_WORK) is Permission.PROHIBITED

    def test_terms_aware_of_a_narrower_kind_answer_for_it(self) -> None:
        assert PUBLIC_WORK_TERMS.permission_for(CommissionKind.PUBLIC_COMMISSION) is Permission.ALLOWED

    def test_restriction_of_only_a_narrower_kind_makes_terms_not_permissive(self) -> None:
        unrestricted: LicenseTerms = License.CC0_1_0.definition.terms
        terms: CommissionTerms = with_public_commission(unrestricted, Permission.PROHIBITED)
        assert unrestricted.is_permissive
        assert not terms.is_permissive

    def test_assessment_follows_the_terms_of_each_license(self, public_commission: CommissionedUse) -> None:
        assert UseAssessment.of(PUBLIC_WORK_LICENSE, public_commission).permission is Permission.ALLOWED
        (restriction,) = UseAssessment.of(License.CC_BY_NC_4_0.definition, public_commission).restrictions
        assert restriction == Restriction(
            license=License.CC_BY_NC_4_0.definition,
            kind=CommissionKind.PUBLIC_COMMISSION,
            permission=Permission.PROHIBITED,
        )
