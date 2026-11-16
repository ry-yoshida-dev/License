from dataclasses import dataclass

from .intended_use import IntendedUse
from .obligation_trigger import ObligationTrigger
from .work_scope import WorkScope


@dataclass(frozen=True, kw_only=True)
class ObligationCondition:
    """
    When an obligation of a license comes into effect: on which kind of use, and for which works.

    Attributes
    ----------
    trigger : ObligationTrigger
        Kind of use that brings the obligation into effect.
    scope : WorkScope
        Forms of the work the obligation concerns, so that it applies only when the use produces one of them.
    """

    trigger: ObligationTrigger
    scope: WorkScope

    def applies_to(self, use: IntendedUse) -> bool:
        """
        Whether an intended use brings the obligation into effect.

        Parameters
        ----------
        use : IntendedUse
            How the work is going to be used.

        Returns
        -------
        bool
            True when the use is of the triggering kind and produces a work within the scope.
        """
        return self.trigger.is_triggered_by(use) and self.scope.covers(use)
