from dataclasses import replace

import pytest

from license_kit import (
    IntendedUse,
    License,
    LicenseChoice,
    LicenseCombination,
    LicenseDefinition,
    Obligation,
    Permission,
    UseAssessment,
)

MIT: LicenseDefinition = License.MIT.definition
APACHE: LicenseDefinition = License.APACHE_2_0.definition
GPL: LicenseDefinition = License.GPL_3_0_ONLY.definition
CC_BY_SA: LicenseDefinition = License.CC_BY_SA_4_0.definition


class TestLicenseCombination:
    def test_alternatives_join_one_pick_from_every_part(self) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(LicenseChoice(options=(MIT, APACHE)), GPL))
        assert combination.alternatives == (frozenset({MIT, GPL}), frozenset({APACHE, GPL}))

    def test_every_part_brings_its_requirements(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(MIT, License.CC_BY_4_0.definition))
        assessment: UseAssessment = UseAssessment.of(combination, replace(private_use, is_redistributed=True))
        assert {(requirement.license, requirement.obligation) for requirement in assessment.requirements} == {
            (MIT, Obligation.ATTRIBUTION),
            (License.CC_BY_4_0.definition, Obligation.ATTRIBUTION),
        }

    def test_restriction_of_one_part_restricts_the_whole(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(MIT, License.CC_BY_NC_4_0.definition))
        assert UseAssessment.of(combination, replace(private_use, is_commercial=True)).permission is (
            Permission.PROHIBITED
        )

    def test_a_choice_inside_is_resolved_for_the_whole_combination(self, private_use: IntendedUse) -> None:
        combination: LicenseCombination = LicenseCombination(parts=(LicenseChoice(options=(CC_BY_SA, GPL)), GPL))
        use: IntendedUse = replace(private_use, is_modified=True, is_combined=True, is_redistributed=True)
        assessment: UseAssessment = UseAssessment.of(combination, use)
        assert assessment.licenses == {GPL}
        assert assessment.permission is Permission.ALLOWED

    def test_single_part_is_refused(self) -> None:
        with pytest.raises(ValueError, match="at least two"):
            _ = LicenseCombination(parts=(MIT,))

    def test_repeated_part_is_refused(self) -> None:
        with pytest.raises(ValueError, match="repeat"):
            _ = LicenseCombination(parts=(MIT, MIT))
