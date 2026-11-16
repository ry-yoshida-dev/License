from collections.abc import Callable
from dataclasses import replace

import pytest

from license_kit import IntendedUse, ObligationTrigger

# Each use as a change to private use, with the triggers it brings into effect.
CASES: dict[str, tuple[Callable[[IntendedUse], IntendedUse], set[ObligationTrigger]]] = {
    "private": (lambda use: use, {ObligationTrigger.ANY_USE}),
    "redistributed": (lambda use: replace(use, is_redistributed=True), set(ObligationTrigger)),
    "network": (
        lambda use: replace(use, is_offered_over_network=True),
        {ObligationTrigger.ANY_USE, ObligationTrigger.REDISTRIBUTION_OR_NETWORK_SERVICE},
    ),
    "modified_network": (
        lambda use: replace(use, is_modified=True, is_offered_over_network=True),
        set(ObligationTrigger) - {ObligationTrigger.REDISTRIBUTION},
    ),
    "combined_network": (
        lambda use: replace(use, is_combined=True, is_offered_over_network=True),
        set(ObligationTrigger) - {ObligationTrigger.REDISTRIBUTION},
    ),
}


class TestObligationTrigger:
    @pytest.mark.parametrize(("derive", "triggered"), list(CASES.values()), ids=list(CASES))
    def test_use_brings_exactly_its_triggers_into_effect(
        self,
        derive: Callable[[IntendedUse], IntendedUse],
        triggered: set[ObligationTrigger],
        private_use: IntendedUse,
    ) -> None:
        use: IntendedUse = derive(private_use)
        assert {trigger for trigger in ObligationTrigger if trigger.is_triggered_by(use)} == triggered
