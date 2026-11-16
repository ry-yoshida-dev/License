from dataclasses import replace

import pytest

from license_kit import (
    IntendedUse,
    License,
    LicenseChoice,
    LicenseCombination,
    LicenseDefinition,
    ObligationCondition,
    ObligationTrigger,
    Permission,
    UseAssessment,
    WorkScope,
)


class TestLicenseChoice:
    def test_alternatives_are_those_of_every_option_in_order(self) -> None:
        choice: LicenseChoice = LicenseChoice(options=(License.MIT.definition, License.APACHE_2_0.definition))
        assert choice.alternatives == (
            frozenset({License.MIT.definition}),
            frozenset({License.APACHE_2_0.definition}),
        )

    def test_the_least_restrictive_permission_is_chosen(self, private_use: IntendedUse) -> None:
        choice: LicenseChoice = LicenseChoice(
            options=(License.CC_BY_NC_4_0.definition, License.GPL_3_0_ONLY.definition)
        )
        use: IntendedUse = replace(private_use, is_commercial=True)
        assert UseAssessment.of(choice, use).licenses == {License.GPL_3_0_ONLY.definition}

    def test_lighter_obligations_are_chosen_over_fewer(self, private_use: IntendedUse) -> None:
        copyleft_only: LicenseDefinition = replace(
            License.CC0_1_0.definition,
            identifier="LicenseRef-Copyleft-Only",
            terms=replace(
                License.CC0_1_0.definition.terms,
                share_alike=ObligationCondition(
                    trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK
                ),
            ),
        )
        choice: LicenseChoice = LicenseChoice(options=(copyleft_only, License.APACHE_2_0.definition))
        use: IntendedUse = replace(private_use, is_modified=True, is_redistributed=True)
        assert UseAssessment.of(choice, use).licenses == {License.APACHE_2_0.definition}

    def test_narrower_copyleft_is_chosen(self, private_use: IntendedUse) -> None:
        choice: LicenseChoice = LicenseChoice(
            options=(License.GPL_3_0_ONLY.definition, License.LGPL_3_0_ONLY.definition)
        )
        use: IntendedUse = replace(private_use, is_modified=True, is_combined=True, is_redistributed=True)
        assert UseAssessment.of(choice, use).licenses == {License.LGPL_3_0_ONLY.definition}

    def test_a_subset_of_obligations_is_chosen(self, private_use: IntendedUse) -> None:
        choice: LicenseChoice = LicenseChoice(options=(License.APACHE_2_0.definition, License.MIT.definition))
        use: IntendedUse = replace(private_use, is_modified=True, is_redistributed=True)
        assert UseAssessment.of(choice, use).licenses == {License.MIT.definition}

    def test_the_listed_order_wins_a_tie(self, private_use: IntendedUse) -> None:
        choice: LicenseChoice = LicenseChoice(options=(License.APACHE_2_0.definition, License.MIT.definition))
        assert UseAssessment.of(choice, private_use).licenses == {License.APACHE_2_0.definition}

    def test_conditional_is_chosen_over_unspecified(self, private_use: IntendedUse) -> None:
        conditional: LicenseDefinition = replace(
            License.MIT.definition,
            identifier="LicenseRef-Conditional",
            terms=replace(License.MIT.definition.terms, non_research_use=Permission.CONDITIONAL),
        )
        unspecified: LicenseDefinition = replace(
            License.MIT.definition,
            identifier="LicenseRef-Unspecified",
            terms=replace(License.MIT.definition.terms, non_research_use=Permission.UNSPECIFIED),
        )
        choice: LicenseChoice = LicenseChoice(options=(unspecified, conditional))
        assert UseAssessment.of(choice, private_use).permission is Permission.CONDITIONAL

    def test_prohibition_is_reported_when_no_option_permits(self, private_use: IntendedUse) -> None:
        choice: LicenseChoice = LicenseChoice(
            options=(License.CC_BY_NC_4_0.definition, License.CC_BY_NC_ND_4_0.definition)
        )
        use: IntendedUse = replace(private_use, is_commercial=True)
        assert UseAssessment.of(choice, use).permission is Permission.PROHIBITED

    def test_options_may_be_combinations(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(
            parts=(License.MIT.definition, License.CC_BY_NC_4_0.definition)
        )
        choice: LicenseChoice = LicenseChoice(options=(combination, License.APACHE_2_0.definition))
        use: IntendedUse = replace(private_use, is_commercial=True)
        assert UseAssessment.of(choice, use).licenses == {License.APACHE_2_0.definition}

    def test_single_option_is_refused(self) -> None:
        with pytest.raises(ValueError, match="at least two"):
            _ = LicenseChoice(options=(License.MIT.definition,))

    def test_repeated_option_is_refused(self) -> None:
        with pytest.raises(ValueError, match="repeat"):
            _ = LicenseChoice(options=(License.MIT.definition, License.MIT.definition))
