from dataclasses import dataclass

from .use_kind import UseKind


@dataclass(frozen=True, kw_only=True)
class IntendedUse:
    """
    How a work is going to be used, item by item, to be assessed against the terms of its license.

    Every item must be stated, so that a use is never assessed on an item its author forgot.

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
    """

    is_commercial: bool
    is_research_only: bool
    is_used_for_ai_training: bool
    is_modified: bool
    is_combined: bool
    is_redistributed: bool
    is_offered_over_network: bool

    @property
    def involved_kinds(self) -> frozenset[UseKind]:
        """
        Kinds of use that a license must permit for this use to go ahead.

        Returns
        -------
        frozenset[UseKind]
            Every kind of use this use involves.
        """
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
