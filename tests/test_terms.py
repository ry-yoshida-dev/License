from collections.abc import Callable
from dataclasses import replace

import pytest

from license_kit import (
    LicenseTerms,
    Obligation,
    ObligationCondition,
    ObligationTrigger,
    Permission,
    UseKind,
    WorkScope,
)

UNRESTRICTED: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=None,
    modification_notice=None,
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
ON_REDISTRIBUTION: ObligationCondition = ObligationCondition(
    trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM
)
# Each kind of use paired with a way to set its permission in the terms; modified redistribution moves with the
# kinds it involves, so that the terms stay consistent.
RESTRICTERS: dict[UseKind, Callable[[Permission], LicenseTerms]] = {
    UseKind.COMMERCIAL_USE: lambda permission: replace(UNRESTRICTED, commercial_use=permission),
    UseKind.NON_RESEARCH_USE: lambda permission: replace(UNRESTRICTED, non_research_use=permission),
    UseKind.AI_TRAINING: lambda permission: replace(UNRESTRICTED, ai_training=permission),
    UseKind.MODIFICATION: lambda permission: replace(
        UNRESTRICTED, modification=permission, modified_redistribution=permission
    ),
    UseKind.REDISTRIBUTION: lambda permission: replace(
        UNRESTRICTED, redistribution=permission, modified_redistribution=permission
    ),
    UseKind.MODIFIED_REDISTRIBUTION: lambda permission: replace(UNRESTRICTED, modified_redistribution=permission),
    UseKind.NETWORK_SERVICE: lambda permission: replace(UNRESTRICTED, network_service=permission),
}
# Each obligation paired with a way to set its condition in the terms.
OBLIGATION_SETTERS: dict[Obligation, Callable[[ObligationCondition], LicenseTerms]] = {
    Obligation.ATTRIBUTION: lambda condition: replace(UNRESTRICTED, attribution=condition),
    Obligation.MODIFICATION_NOTICE: lambda condition: replace(UNRESTRICTED, modification_notice=condition),
    Obligation.SOURCE_DISCLOSURE: lambda condition: replace(UNRESTRICTED, source_disclosure=condition),
    Obligation.DOWNSTREAM_TERMS: lambda condition: replace(UNRESTRICTED, downstream_terms=condition),
    Obligation.SHARE_ALIKE: lambda condition: replace(UNRESTRICTED, share_alike=condition),
}


class TestLicenseTerms:
    def test_every_kind_and_obligation_can_be_set(self) -> None:
        assert set(RESTRICTERS) == set(UseKind)
        assert set(OBLIGATION_SETTERS) == set(Obligation)

    @pytest.mark.parametrize("kind", list(UseKind))
    def test_permission_for_reads_the_item_of_the_kind(self, kind: UseKind) -> None:
        terms: LicenseTerms = RESTRICTERS[kind](Permission.PROHIBITED)
        assert terms.permission_for(kind) is Permission.PROHIBITED

    @pytest.mark.parametrize("obligation", list(Obligation))
    def test_condition_for_reads_the_item_of_the_obligation(self, obligation: Obligation) -> None:
        terms: LicenseTerms = OBLIGATION_SETTERS[obligation](ON_REDISTRIBUTION)
        assert terms.condition_for(obligation) == ON_REDISTRIBUTION
        assert all(terms.condition_for(other) is None for other in Obligation if other is not obligation)

    def test_unrestricted_terms_are_permissive(self) -> None:
        assert UNRESTRICTED.is_permissive

    @pytest.mark.parametrize("kind", list(UseKind))
    @pytest.mark.parametrize("permission", [Permission.CONDITIONAL, Permission.UNSPECIFIED, Permission.PROHIBITED])
    def test_any_restricted_kind_is_not_permissive(self, kind: UseKind, permission: Permission) -> None:
        assert not RESTRICTERS[kind](permission).is_permissive

    def test_only_releasing_obligations_make_terms_not_permissive(self) -> None:
        condition: ObligationCondition = ObligationCondition(
            trigger=ObligationTrigger.ANY_USE, scope=WorkScope.MODIFIED_WORK
        )
        assert {
            obligation for obligation in Obligation if not OBLIGATION_SETTERS[obligation](condition).is_permissive
        } == {Obligation.SOURCE_DISCLOSURE, Obligation.DOWNSTREAM_TERMS, Obligation.SHARE_ALIKE}

    def test_modified_redistribution_looser_than_modification_is_refused(self) -> None:
        with pytest.raises(ValueError, match="modified_redistribution"):
            _ = replace(UNRESTRICTED, modification=Permission.PROHIBITED)

    def test_modified_redistribution_looser_than_redistribution_is_refused(self) -> None:
        with pytest.raises(ValueError, match="modified_redistribution"):
            _ = replace(UNRESTRICTED, redistribution=Permission.CONDITIONAL)
