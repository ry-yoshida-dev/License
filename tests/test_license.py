from dataclasses import replace

import pytest

from license_kit import IntendedUse, License, LicenseDefinition, Obligation, Permission, UseAssessment

ATTRIBUTION: Obligation = Obligation.ATTRIBUTION
MODIFICATION_NOTICE: Obligation = Obligation.MODIFICATION_NOTICE
SOURCE_DISCLOSURE: Obligation = Obligation.SOURCE_DISCLOSURE
DOWNSTREAM_TERMS: Obligation = Obligation.DOWNSTREAM_TERMS
SHARE_ALIKE: Obligation = Obligation.SHARE_ALIKE
ALLOWED: Permission = Permission.ALLOWED
PROHIBITED: Permission = Permission.PROHIBITED

# Golden tables written from the license texts, not from the presets, one per canonical use.
COMMERCIAL_USE: dict[License, Permission] = {
    License.MIT: ALLOWED,
    License.BSD_2_CLAUSE: ALLOWED,
    License.BSD_3_CLAUSE: ALLOWED,
    License.APACHE_2_0: ALLOWED,
    License.MPL_2_0: ALLOWED,
    License.LGPL_2_1_ONLY: ALLOWED,
    License.LGPL_2_1_OR_LATER: ALLOWED,
    License.LGPL_3_0_ONLY: ALLOWED,
    License.LGPL_3_0_OR_LATER: ALLOWED,
    License.GPL_2_0_ONLY: ALLOWED,
    License.GPL_2_0_OR_LATER: ALLOWED,
    License.GPL_3_0_ONLY: ALLOWED,
    License.GPL_3_0_OR_LATER: ALLOWED,
    License.AGPL_3_0_ONLY: ALLOWED,
    License.AGPL_3_0_OR_LATER: ALLOWED,
    License.CC0_1_0: ALLOWED,
    License.CC_BY_4_0: ALLOWED,
    License.CC_BY_SA_4_0: ALLOWED,
    License.CC_BY_ND_4_0: ALLOWED,
    License.CC_BY_NC_4_0: PROHIBITED,
    License.CC_BY_NC_SA_4_0: PROHIBITED,
    License.CC_BY_NC_ND_4_0: PROHIBITED,
    License.ODBL_1_0: ALLOWED,
    License.PUBLIC_DATA_LICENSE_1_0: ALLOWED,
    License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL: PROHIBITED,
}
SHIPPING_MODIFIED_PERMISSION: dict[License, Permission] = {
    License.MIT: ALLOWED,
    License.BSD_2_CLAUSE: ALLOWED,
    License.BSD_3_CLAUSE: ALLOWED,
    License.APACHE_2_0: ALLOWED,
    License.MPL_2_0: ALLOWED,
    License.LGPL_2_1_ONLY: ALLOWED,
    License.LGPL_2_1_OR_LATER: ALLOWED,
    License.LGPL_3_0_ONLY: ALLOWED,
    License.LGPL_3_0_OR_LATER: ALLOWED,
    License.GPL_2_0_ONLY: ALLOWED,
    License.GPL_2_0_OR_LATER: ALLOWED,
    License.GPL_3_0_ONLY: ALLOWED,
    License.GPL_3_0_OR_LATER: ALLOWED,
    License.AGPL_3_0_ONLY: ALLOWED,
    License.AGPL_3_0_OR_LATER: ALLOWED,
    License.CC0_1_0: ALLOWED,
    License.CC_BY_4_0: ALLOWED,
    License.CC_BY_SA_4_0: ALLOWED,
    License.CC_BY_ND_4_0: PROHIBITED,
    License.CC_BY_NC_4_0: ALLOWED,
    License.CC_BY_NC_SA_4_0: ALLOWED,
    License.CC_BY_NC_ND_4_0: PROHIBITED,
    License.ODBL_1_0: ALLOWED,
    License.PUBLIC_DATA_LICENSE_1_0: ALLOWED,
    License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL: PROHIBITED,
}
SHIPPING_MODIFIED_OBLIGATIONS: dict[License, set[Obligation]] = {
    License.MIT: {ATTRIBUTION},
    License.BSD_2_CLAUSE: {ATTRIBUTION},
    License.BSD_3_CLAUSE: {ATTRIBUTION},
    License.APACHE_2_0: {ATTRIBUTION, MODIFICATION_NOTICE},
    License.MPL_2_0: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.LGPL_2_1_ONLY: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS, SHARE_ALIKE},
    License.LGPL_2_1_OR_LATER: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS, SHARE_ALIKE},
    License.LGPL_3_0_ONLY: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS, SHARE_ALIKE},
    License.LGPL_3_0_OR_LATER: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS, SHARE_ALIKE},
    License.GPL_2_0_ONLY: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.GPL_2_0_OR_LATER: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.GPL_3_0_ONLY: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.GPL_3_0_OR_LATER: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.AGPL_3_0_ONLY: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.AGPL_3_0_OR_LATER: {ATTRIBUTION, MODIFICATION_NOTICE, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.CC0_1_0: set(),
    License.CC_BY_4_0: {ATTRIBUTION, MODIFICATION_NOTICE},
    License.CC_BY_SA_4_0: {ATTRIBUTION, MODIFICATION_NOTICE, SHARE_ALIKE},
    License.CC_BY_ND_4_0: {ATTRIBUTION, MODIFICATION_NOTICE},
    License.CC_BY_NC_4_0: {ATTRIBUTION, MODIFICATION_NOTICE},
    License.CC_BY_NC_SA_4_0: {ATTRIBUTION, MODIFICATION_NOTICE, SHARE_ALIKE},
    License.CC_BY_NC_ND_4_0: {ATTRIBUTION, MODIFICATION_NOTICE},
    License.ODBL_1_0: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.PUBLIC_DATA_LICENSE_1_0: {ATTRIBUTION, MODIFICATION_NOTICE},
    License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL: {ATTRIBUTION, MODIFICATION_NOTICE, DOWNSTREAM_TERMS},
}
SHIPPING_COMBINED_OBLIGATIONS: dict[License, set[Obligation]] = {
    License.MIT: {ATTRIBUTION},
    License.BSD_2_CLAUSE: {ATTRIBUTION},
    License.BSD_3_CLAUSE: {ATTRIBUTION},
    License.APACHE_2_0: {ATTRIBUTION},
    License.MPL_2_0: {ATTRIBUTION, SOURCE_DISCLOSURE},
    License.LGPL_2_1_ONLY: {ATTRIBUTION, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS},
    License.LGPL_2_1_OR_LATER: {ATTRIBUTION, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS},
    License.LGPL_3_0_ONLY: {ATTRIBUTION, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS},
    License.LGPL_3_0_OR_LATER: {ATTRIBUTION, SOURCE_DISCLOSURE, DOWNSTREAM_TERMS},
    License.GPL_2_0_ONLY: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.GPL_2_0_OR_LATER: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.GPL_3_0_ONLY: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.GPL_3_0_OR_LATER: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.AGPL_3_0_ONLY: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.AGPL_3_0_OR_LATER: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.CC0_1_0: set(),
    License.CC_BY_4_0: {ATTRIBUTION},
    License.CC_BY_SA_4_0: {ATTRIBUTION},
    License.CC_BY_ND_4_0: {ATTRIBUTION},
    License.CC_BY_NC_4_0: {ATTRIBUTION},
    License.CC_BY_NC_SA_4_0: {ATTRIBUTION},
    License.CC_BY_NC_ND_4_0: {ATTRIBUTION},
    License.ODBL_1_0: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.PUBLIC_DATA_LICENSE_1_0: {ATTRIBUTION},
    License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL: {ATTRIBUTION},
}
SERVING_MODIFIED_OBLIGATIONS: dict[License, set[Obligation]] = {
    License.MIT: set(),
    License.BSD_2_CLAUSE: set(),
    License.BSD_3_CLAUSE: set(),
    License.APACHE_2_0: set(),
    License.MPL_2_0: set(),
    License.LGPL_2_1_ONLY: set(),
    License.LGPL_2_1_OR_LATER: set(),
    License.LGPL_3_0_ONLY: set(),
    License.LGPL_3_0_OR_LATER: set(),
    License.GPL_2_0_ONLY: set(),
    License.GPL_2_0_OR_LATER: set(),
    License.GPL_3_0_ONLY: set(),
    License.GPL_3_0_OR_LATER: set(),
    License.AGPL_3_0_ONLY: {SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.AGPL_3_0_OR_LATER: {SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.CC0_1_0: set(),
    License.CC_BY_4_0: set(),
    License.CC_BY_SA_4_0: set(),
    License.CC_BY_ND_4_0: set(),
    License.CC_BY_NC_4_0: set(),
    License.CC_BY_NC_SA_4_0: set(),
    License.CC_BY_NC_ND_4_0: set(),
    License.ODBL_1_0: {ATTRIBUTION, SOURCE_DISCLOSURE, SHARE_ALIKE},
    License.PUBLIC_DATA_LICENSE_1_0: set(),
    License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL: set(),
}
GOLDEN_TABLES: list[dict[License, Permission] | dict[License, set[Obligation]]] = [
    COMMERCIAL_USE,
    SHIPPING_MODIFIED_PERMISSION,
    SHIPPING_MODIFIED_OBLIGATIONS,
    SHIPPING_COMBINED_OBLIGATIONS,
    SERVING_MODIFIED_OBLIGATIONS,
]


def _obligations(member: License, use: IntendedUse) -> set[Obligation]:
    return {requirement.obligation for requirement in UseAssessment.of(member.definition, use).requirements}


class TestLicense:
    def test_golden_tables_cover_every_license(self) -> None:
        assert all(set(table) == set(License) for table in GOLDEN_TABLES)

    @pytest.mark.parametrize("member", list(License))
    def test_definition_carries_the_identifier(self, member: License) -> None:
        assert member.definition.identifier == member.value

    def test_titles_are_unique(self) -> None:
        assert len({member.definition.title for member in License}) == len(License)

    def test_short_titles_are_unique(self) -> None:
        assert len({member.definition.short_title for member in License}) == len(License)

    def test_only_apple_research_license_lacks_a_canonical_page(self) -> None:
        assert {member for member in License if member.definition.url is None} == {
            License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL
        }

    def test_permissive_licenses(self) -> None:
        assert {member for member in License if member.definition.terms.is_permissive} == {
            License.MIT,
            License.BSD_2_CLAUSE,
            License.BSD_3_CLAUSE,
            License.APACHE_2_0,
            License.CC0_1_0,
            License.CC_BY_4_0,
            License.PUBLIC_DATA_LICENSE_1_0,
        }

    @pytest.mark.parametrize("member", list(License))
    def test_commercial_use(self, member: License, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_commercial=True)
        assert UseAssessment.of(member.definition, use).permission is COMMERCIAL_USE[member]

    @pytest.mark.parametrize("member", list(License))
    def test_shipping_a_modified_copy(self, member: License, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_modified=True, is_redistributed=True)
        assert UseAssessment.of(member.definition, use).permission is SHIPPING_MODIFIED_PERMISSION[member]
        assert _obligations(member, use) == SHIPPING_MODIFIED_OBLIGATIONS[member]

    @pytest.mark.parametrize("member", list(License))
    def test_shipping_a_work_combined_with_it(self, member: License, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_combined=True, is_redistributed=True)
        assert _obligations(member, use) == SHIPPING_COMBINED_OBLIGATIONS[member]

    @pytest.mark.parametrize("member", list(License))
    def test_serving_a_modified_version_over_a_network(self, member: License, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_modified=True, is_offered_over_network=True)
        assert _obligations(member, use) == SERVING_MODIFIED_OBLIGATIONS[member]

    @pytest.mark.parametrize("member", list(License))
    def test_private_use_brings_no_obligation(self, member: License, private_use: IntendedUse) -> None:
        assert _obligations(member, private_use) == set()

    def test_apple_research_license_allows_research_and_training(self, private_use: IntendedUse) -> None:
        definition: LicenseDefinition = License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL.definition
        use: IntendedUse = replace(private_use, is_research_only=True, is_used_for_ai_training=True)
        assert UseAssessment.of(definition, use).permission is ALLOWED

    def test_unmodified_agpl_served_over_a_network_brings_no_obligation(self, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_offered_over_network=True)
        assert _obligations(License.AGPL_3_0_ONLY, use) == set()
