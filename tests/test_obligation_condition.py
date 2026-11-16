from dataclasses import replace

from license_kit import IntendedUse, ObligationCondition, ObligationTrigger, WorkScope


class TestObligationCondition:
    def test_scoped_condition_applies_only_when_scope_and_trigger_both_hold(self, private_use: IntendedUse) -> None:
        condition: ObligationCondition = ObligationCondition(
            trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK
        )
        assert not condition.applies_to(replace(private_use, is_modified=True))
        assert not condition.applies_to(replace(private_use, is_redistributed=True))
        assert condition.applies_to(replace(private_use, is_modified=True, is_redistributed=True))

    def test_unscoped_condition_applies_to_the_work_as_is(self, private_use: IntendedUse) -> None:
        condition: ObligationCondition = ObligationCondition(
            trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM
        )
        assert condition.applies_to(replace(private_use, is_redistributed=True))
        assert not condition.applies_to(private_use)

    def test_scoped_any_use_condition_applies_to_private_modification(self, private_use: IntendedUse) -> None:
        condition: ObligationCondition = ObligationCondition(
            trigger=ObligationTrigger.ANY_USE, scope=WorkScope.MODIFIED_WORK
        )
        assert condition.applies_to(replace(private_use, is_modified=True))
        assert not condition.applies_to(private_use)
