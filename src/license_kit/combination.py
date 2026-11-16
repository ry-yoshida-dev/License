from dataclasses import dataclass
from itertools import product

from .definition import LicenseDefinition
from .expression import LicenseExpression


@dataclass(frozen=True, kw_only=True)
class LicenseCombination:
    """
    Licensings that all apply to a work at once (an SPDX ``AND`` expression).

    A typical case is a package bundling files under different licenses, used as one. Separate works used in
    different ways, such as code that is modified and weights that are not, are assessed one by one instead.

    Attributes
    ----------
    parts : tuple[LicenseExpression, ...]
        Licensings to comply with together.

    Raises
    ------
    ValueError
        If fewer than two parts are given or a part is repeated.
    """

    parts: tuple[LicenseExpression, ...]

    def __post_init__(self) -> None:
        if len(self.parts) < 2:
            raise ValueError("parts must contain at least two licensings.")
        if len(set(self.parts)) != len(self.parts):
            raise ValueError("parts must not repeat a licensing.")

    @property
    def alternatives(self) -> tuple[frozenset[LicenseDefinition], ...]:
        """
        Every way the licensing can be complied with.

        Returns
        -------
        tuple[frozenset[LicenseDefinition], ...]
            One set for each way of picking an alternative of every part, joining the licenses of the picks.
        """
        return tuple(
            frozenset[LicenseDefinition]().union(*picks)
            for picks in product(*(part.alternatives for part in self.parts))
        )
