from dataclasses import dataclass

from .definition import LicenseDefinition
from .obligation import Obligation
from .obligation_condition import ObligationCondition


@dataclass(frozen=True, kw_only=True)
class Requirement:
    """
    Obligation that an intended use brings into effect under one license.

    Attributes
    ----------
    license : LicenseDefinition
        License that imposes the obligation, such as the one whose notice to keep or under which to share alike.
    obligation : Obligation
        Duty to fulfil.
    condition : ObligationCondition
        Condition under which the license imposes it, whose scope tells how far the duty reaches.
    """

    license: LicenseDefinition
    obligation: Obligation
    condition: ObligationCondition
