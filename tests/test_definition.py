from dataclasses import replace

import pytest

from license_kit import License, LicenseDefinition, LicenseTerms

TERMS: LicenseTerms = License.CC_BY_NC_4_0.definition.terms
CUSTOM: LicenseDefinition = LicenseDefinition(
    title="Municipal dataset terms",
    short_title="Municipal data",
    terms=TERMS,
    identifier="LicenseRef-Municipal-Data",
    url="https://example.com/terms",
)


class TestLicenseDefinition:
    def test_custom_and_well_known_definitions_are_hashable_together(self) -> None:
        assert len({CUSTOM, License.CC_BY_NC_4_0.definition, License.CC_BY_NC_4_0.definition}) == 2

    def test_single_license_is_its_only_alternative(self) -> None:
        assert CUSTOM.alternatives == (frozenset({CUSTOM}),)

    def test_identifier_and_url_may_be_absent(self) -> None:
        definition: LicenseDefinition = replace(CUSTOM, identifier=None, url=None)
        assert definition.identifier is None
        assert definition.url is None

    @pytest.mark.parametrize("title", ["", "   "])
    def test_blank_title_is_refused(self, title: str) -> None:
        with pytest.raises(ValueError, match="title"):
            _ = replace(CUSTOM, title=title)

    @pytest.mark.parametrize("short_title", ["", "   "])
    def test_blank_short_title_is_refused(self, short_title: str) -> None:
        with pytest.raises(ValueError, match="short_title"):
            _ = replace(CUSTOM, short_title=short_title)

    @pytest.mark.parametrize(
        "identifier", ["", "-", ".MIT", "MIT OR Apache-2.0", "LicenseRef-Data_1", "LicenseRef-データ"]
    )
    def test_identifier_outside_spdx_characters_is_refused(self, identifier: str) -> None:
        with pytest.raises(ValueError, match="identifier"):
            _ = replace(CUSTOM, identifier=identifier)

    @pytest.mark.parametrize("url", ["", "   ", "example.com/terms", "ftp://example.com/terms", "https://"])
    def test_url_other_than_absolute_http_is_refused(self, url: str) -> None:
        with pytest.raises(ValueError, match="url"):
            _ = replace(CUSTOM, url=url)
