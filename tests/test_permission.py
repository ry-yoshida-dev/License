import pytest

from license_kit import Permission

ORDER_FROM_LEAST_RESTRICTIVE: list[Permission] = [
    Permission.ALLOWED,
    Permission.CONDITIONAL,
    Permission.UNSPECIFIED,
    Permission.PROHIBITED,
]


class TestPermission:
    def test_restrictiveness_follows_the_order(self) -> None:
        assert [permission.restrictiveness for permission in ORDER_FROM_LEAST_RESTRICTIVE] == [0, 1, 2, 3]
        assert set(ORDER_FROM_LEAST_RESTRICTIVE) == set(Permission)

    @pytest.mark.parametrize("first", list(Permission))
    @pytest.mark.parametrize("second", list(Permission))
    def test_combine_gives_the_more_restrictive(self, first: Permission, second: Permission) -> None:
        expected: Permission = max(first, second, key=ORDER_FROM_LEAST_RESTRICTIVE.index)
        assert first.combine(second) is expected
        assert second.combine(first) is expected
