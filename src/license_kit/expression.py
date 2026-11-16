from collections.abc import Hashable
from typing import Protocol

from .definition import LicenseDefinition


class LicenseExpression(Hashable, Protocol):
    """
    Licensing of a work: a license, a choice among licensings (SPDX ``OR``), or licensings applying at once (``AND``).

    `LicenseDefinition`, `LicenseChoice`, and `LicenseCombination` satisfy it, and nest in one another, so that packages
    declare any licensing alike and `UseAssessment.of` assesses it.
    """

    @property
    def alternatives(self) -> tuple[frozenset[LicenseDefinition], ...]:
        """
        Every way the licensing can be complied with.

        Returns
        -------
        tuple[frozenset[LicenseDefinition], ...]
            Sets of licenses that apply together, one set per combination of choices, in the order the choices list
            their options.
        """
        ...
