import pytest

from license_kit import License, Permission, Restriction, UseKind


class TestRestriction:
    def test_allowed_kind_is_not_a_restriction(self) -> None:
        with pytest.raises(ValueError, match="not a restriction"):
            _ = Restriction(license=License.MIT.definition, kind=UseKind.COMMERCIAL_USE, permission=Permission.ALLOWED)
