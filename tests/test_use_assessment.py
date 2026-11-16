from dataclasses import replace

from license_kit import (
    IntendedUse,
    License,
    LicenseCombination,
    LicenseDefinition,
    LicenseTerms,
    Obligation,
    ObligationCondition,
    ObligationTrigger,
    Permission,
    Requirement,
    Restriction,
    UseAssessment,
    UseKind,
    WorkScope,
)

CUSTOM: LicenseDefinition = LicenseDefinition(
    title="Municipal dataset terms",
    terms=License.CC_BY_NC_4_0.definition.terms,
    identifier="LicenseRef-Municipal-Data",
    url=None,
)
GPL: LicenseDefinition = License.GPL_3_0_ONLY.definition


class TestUseAssessment:
    def test_restrictions_and_requirements_are_attributed_to_the_license(self, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_commercial=True, is_redistributed=True)
        assessment: UseAssessment = UseAssessment.of(CUSTOM, use)
        assert assessment.licenses == {CUSTOM}
        assert assessment.restrictions == {
            Restriction(license=CUSTOM, kind=UseKind.COMMERCIAL_USE, permission=Permission.PROHIBITED)
        }
        assert assessment.requirements == {
            Requirement(
                license=CUSTOM,
                obligation=Obligation.ATTRIBUTION,
                condition=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
            )
        }
        assert assessment.permission is Permission.PROHIBITED

    def test_allowed_use_has_no_restriction(self, private_use: IntendedUse) -> None:
        assessment: UseAssessment = UseAssessment.of(CUSTOM, private_use)
        assert assessment.restrictions == frozenset()
        assert assessment.permission is Permission.ALLOWED

    def test_permission_is_the_most_restrictive_restriction(self, private_use: IntendedUse) -> None:
        terms: LicenseTerms = replace(
            License.MIT.definition.terms, commercial_use=Permission.CONDITIONAL, non_research_use=Permission.UNSPECIFIED
        )
        definition: LicenseDefinition = replace(CUSTOM, terms=terms)
        use: IntendedUse = replace(private_use, is_commercial=True)
        assert UseAssessment.of(definition, use).permission is Permission.UNSPECIFIED

    def test_any_use_obligation_applies_to_private_use(self, private_use: IntendedUse) -> None:
        condition: ObligationCondition = ObligationCondition(
            trigger=ObligationTrigger.ANY_USE, scope=WorkScope.ANY_FORM
        )
        definition: LicenseDefinition = replace(CUSTOM, terms=replace(CUSTOM.terms, attribution=condition))
        assert {requirement.obligation for requirement in UseAssessment.of(definition, private_use).requirements} == {
            Obligation.ATTRIBUTION
        }

    def test_one_copyleft_license_is_no_conflict(self, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_modified=True, is_redistributed=True)
        assessment: UseAssessment = UseAssessment.of(GPL, use)
        assert assessment.conflicts == frozenset()
        assert assessment.permission is Permission.ALLOWED

    def test_copyleft_of_two_licenses_must_be_confirmed(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(GPL, License.CC_BY_SA_4_0.definition))
        use: IntendedUse = replace(private_use, is_modified=True, is_redistributed=True)
        assessment: UseAssessment = UseAssessment.of(combination, use)
        assert assessment.conflicts == {GPL, License.CC_BY_SA_4_0.definition}
        assert assessment.restrictions == frozenset()
        assert assessment.permission is Permission.UNSPECIFIED

    def test_file_level_copyleft_does_not_conflict(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(GPL, License.MPL_2_0.definition))
        use: IntendedUse = replace(private_use, is_modified=True, is_combined=True, is_redistributed=True)
        assert UseAssessment.of(combination, use).conflicts == frozenset()

    def test_requirement_carries_how_far_copyleft_reaches(self, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_modified=True, is_redistributed=True)
        (share_alike,) = (
            requirement
            for requirement in UseAssessment.of(License.MPL_2_0.definition, use).requirements
            if requirement.obligation is Obligation.SHARE_ALIKE
        )
        assert share_alike.condition == License.MPL_2_0.definition.terms.share_alike

    def test_copyleft_over_a_combined_work_conflicts_with_added_restrictions(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(GPL, License.CC_BY_NC_4_0.definition))
        use: IntendedUse = replace(private_use, is_combined=True, is_redistributed=True)
        assessment: UseAssessment = UseAssessment.of(combination, use)
        assert assessment.conflicts == {GPL, License.CC_BY_NC_4_0.definition}
        assert assessment.permission is Permission.UNSPECIFIED

    def test_copyleft_over_a_combined_work_accepts_permissive_licenses(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(GPL, License.MIT.definition))
        use: IntendedUse = replace(private_use, is_combined=True, is_redistributed=True)
        assert UseAssessment.of(combination, use).conflicts == frozenset()

    def test_adaptation_under_share_alike_conflicts_with_added_restrictions(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(
            parts=(License.CC_BY_SA_4_0.definition, License.CC_BY_NC_4_0.definition)
        )
        use: IntendedUse = replace(private_use, is_modified=True, is_combined=True, is_redistributed=True)
        assert UseAssessment.of(combination, use).conflicts == {
            License.CC_BY_SA_4_0.definition,
            License.CC_BY_NC_4_0.definition,
        }
