from dataclasses import dataclass

from .definition import LicenseDefinition
from .narrower_use_kind import NarrowerUseKind
from .permission import Permission
from .use_kind import UseKind


@dataclass(frozen=True, kw_only=True)
class Restriction:
    """
    Kind of use that a license does not plainly allow, found while assessing an intended use.

    Attributes
    ----------
    license : LicenseDefinition
        License that restricts the use.
    kind : UseKind | NarrowerUseKind
        Kind of use it restricts.
    permission : Permission
        What the license states for that kind of use.

    Raises
    ------
    ValueError
        If the permission is ``ALLOWED``, which restricts nothing.
    """

    license: LicenseDefinition
    kind: UseKind | NarrowerUseKind
    permission: Permission

    def __post_init__(self) -> None:
        if self.permission is Permission.ALLOWED:
            raise ValueError(f"{self.kind} is allowed, so it is not a restriction.")
