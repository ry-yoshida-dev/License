from dataclasses import replace

import pytest

from license_kit import IntendedUse, WorkScope


class TestWorkScope:
    def test_any_form_covers_the_work_as_is(self, private_use: IntendedUse) -> None:
        assert {scope for scope in WorkScope if scope.covers(private_use)} == {WorkScope.ANY_FORM}

    @pytest.mark.parametrize("scope", list(WorkScope))
    def test_every_scope_covers_modification(self, scope: WorkScope, private_use: IntendedUse) -> None:
        assert scope.covers(replace(private_use, is_modified=True))

    def test_only_broad_scopes_cover_combination(self, private_use: IntendedUse) -> None:
        combined: IntendedUse = replace(private_use, is_combined=True)
        assert {scope for scope in WorkScope if scope.covers(combined)} == {WorkScope.ANY_FORM, WorkScope.COMBINED_WORK}

    def test_breadth_ranks_any_form_widest(self) -> None:
        assert sorted(WorkScope, key=lambda scope: scope.breadth) == [
            WorkScope.MODIFIED_FILES,
            WorkScope.MODIFIED_WORK,
            WorkScope.COMBINED_WORK,
            WorkScope.ANY_FORM,
        ]
