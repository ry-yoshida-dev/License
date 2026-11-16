from dataclasses import dataclass

from .definition import LicenseDefinition
from .expression import LicenseExpression


@dataclass(frozen=True, kw_only=True)
class LicenseChoice:
    """
    Licensings a work is offered under, any one of which the user may choose (an SPDX ``OR`` expression).

    Typical cases are dual-licensed code such as ``MIT OR Apache-2.0``.

    Attributes
    ----------
    options : tuple[LicenseExpression, ...]
        Licensings to choose from, in the order the licensor lists them.

    Raises
    ------
    ValueError
        If fewer than two options are given or an option is repeated.
    """

    options: tuple[LicenseExpression, ...]

    def __post_init__(self) -> None:
        if len(self.options) < 2:
            raise ValueError("options must contain at least two licensings.")
        if len(set(self.options)) != len(self.options):
            raise ValueError("options must not repeat a licensing.")

    @property
    def alternatives(self) -> tuple[frozenset[LicenseDefinition], ...]:
        """
        Every way the licensing can be complied with.

        Returns
        -------
        tuple[frozenset[LicenseDefinition], ...]
            The alternatives of every option, option by option.
        """
        return tuple(alternative for option in self.options for alternative in option.alternatives)
