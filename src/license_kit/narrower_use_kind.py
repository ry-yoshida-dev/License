from collections.abc import Hashable
from typing import Protocol

from .use_kind import UseKind


class NarrowerUseKind(Hashable, Protocol):
    """
    Kind of use that narrows a broader one, for terms that draw a finer line than `UseKind` does.

    Packages define their own, typically as members of an `Enum`, when terms they describe treat part of a kind of use
    differently from the rest, such as data whose terms forbid commercial use except for work commissioned by a
    public body. A subclass of `IntendedUse` names the narrower kinds a use involves, in place of the broader kinds
    they narrow, and a subclass of `LicenseTerms` states its permission for the narrower kinds it knows. Terms that do
    not know a narrower kind answer with their permission for the broader one, so that well-known licenses apply
    unchanged.
    """

    @property
    def broader(self) -> "UseKind | NarrowerUseKind":
        """
        Kind of use this kind narrows.

        Returns
        -------
        UseKind | NarrowerUseKind
            The broader kind, itself possibly narrowing another, which ends in a `UseKind`.
        """
        ...


def find_broader_kinds(kind: NarrowerUseKind) -> tuple["UseKind | NarrowerUseKind", ...]:
    """
    Every kind of use that a narrower kind narrows, directly or through others.

    Parameters
    ----------
    kind : NarrowerUseKind
        Narrower kind of use.

    Returns
    -------
    tuple[UseKind | NarrowerUseKind, ...]
        The broader kinds from the nearest to the `UseKind` at the end.

    Raises
    ------
    ValueError
        If the chain of broader kinds returns to a kind it has passed.
    """
    chain: list[UseKind | NarrowerUseKind] = []
    current: UseKind | NarrowerUseKind = kind
    while not isinstance(current, UseKind):
        current = current.broader
        if current in chain or current == kind:
            raise ValueError(f"The broader kinds of {kind!r} form a cycle.")
        chain.append(current)
    return tuple(chain)
