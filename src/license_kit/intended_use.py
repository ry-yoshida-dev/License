from dataclasses import dataclass

from .narrower_use_kind import NarrowerUseKind, find_broader_kinds
from .use_kind import UseKind


@dataclass(frozen=True, kw_only=True)
class IntendedUse:
    """
    How a work is going to be used, item by item, to be assessed against the terms of its license.

    Every item must be stated, so that a use is never assessed on an item its author forgot. Packages whose terms
    draw finer lines subclass it, add the items they need, and override `narrower_kinds`.

    Attributes
    ----------
    is_commercial : bool
        Whether the work is used in commercial products, services, or business.
    is_research_only : bool
        Whether the work is used only for scientific research or academic development.
    is_used_for_ai_training : bool
        Whether the work is used to train or fine-tune machine learning models. Training alone neither modifies the
        work nor redistributes it; set those items only when an adaptation or copy of the work itself is made or
        shared. Fine-tuning a model that is itself the licensed work modifies it.
    is_modified : bool
        Whether the work itself is edited, processed, or adapted into a derivative work, including synchronizing media
        with other material.
    is_combined : bool
        Whether the work forms a single work together with other material, such as a library linked into a program.
        For a database, merging its contents into another database. Placing it side by side with other works in a
        distribution or collection is not combination.
    is_redistributed : bool
        Whether copies of the work, as is or modified, are made available to third parties. Publishing or displaying
        the content of the work itself to them, such as images or records shown in a web application, counts too.
    is_offered_over_network : bool
        Whether third parties use software or a model that runs the work over a network without receiving copies of
        it, such as a hosted application or an inference API.

    Raises
    ------
    ValueError
        If a narrower kind of use narrows a kind the items do not involve.
    """

    is_commercial: bool
    is_research_only: bool
    is_used_for_ai_training: bool
    is_modified: bool
    is_combined: bool
    is_redistributed: bool
    is_offered_over_network: bool

    def __post_init__(self) -> None:
        broad_kinds: frozenset[UseKind] = self._broad_kinds
        for kind in self.narrower_kinds:
            broadest: UseKind | NarrowerUseKind = find_broader_kinds(kind)[-1]
            if broadest not in broad_kinds:
                raise ValueError(f"{kind!r} narrows {broadest}, which this use does not involve.")

    @property
    def narrower_kinds(self) -> frozenset[NarrowerUseKind]:
        """
        Narrower kinds of use this use involves, in place of the broader kinds they narrow.

        Subclasses override it to tell the narrower kinds their items bring in, each narrowing a kind the items of
        this class involve.

        Returns
        -------
        frozenset[NarrowerUseKind]
            None here.
        """
        return frozenset()

    @property
    def involved_kinds(self) -> frozenset[UseKind | NarrowerUseKind]:
        """
        Kinds of use that a license must permit for this use to go ahead.

        Returns
        -------
        frozenset[UseKind | NarrowerUseKind]
            Every kind of use this use involves, with each narrower kind in place of the kinds it narrows.
        """
        narrower: frozenset[NarrowerUseKind] = self.narrower_kinds
        replaced: set[UseKind | NarrowerUseKind] = {
            broader for kind in narrower for broader in find_broader_kinds(kind)
        }
        return frozenset((self._broad_kinds | narrower) - replaced)

    @property
    def _broad_kinds(self) -> frozenset[UseKind]:
        kinds: set[UseKind] = set()
        if self.is_commercial:
            kinds.add(UseKind.COMMERCIAL_USE)
        if not self.is_research_only:
            kinds.add(UseKind.NON_RESEARCH_USE)
        if self.is_used_for_ai_training:
            kinds.add(UseKind.AI_TRAINING)
        if self.is_modified:
            kinds.add(UseKind.MODIFICATION)
        if self.is_redistributed:
            kinds.add(UseKind.REDISTRIBUTION)
        if self.is_redistributed and self.is_modified:
            kinds.add(UseKind.MODIFIED_REDISTRIBUTION)
        if self.is_offered_over_network:
            kinds.add(UseKind.NETWORK_SERVICE)
        return frozenset(kinds)
