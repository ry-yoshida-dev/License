from dataclasses import dataclass

from .narrower_use_kind import NarrowerUseKind
from .obligation import Obligation
from .obligation_condition import ObligationCondition
from .permission import Permission
from .use_kind import UseKind


@dataclass(frozen=True, kw_only=True)
class LicenseTerms:
    """
    Terms of a license, item by item: which kinds of use it permits, and when each obligation comes into effect.

    Terms that treat a narrower kind of use differently from the kind it narrows are a subclass that adds an item for
    it, overrides `permission_for` to read that item, and extends `stated_kinds`.

    Attributes
    ----------
    commercial_use : Permission
        Use in commercial products, services, or business.
    non_research_use : Permission
        Use for purposes other than scientific research or academic development.
    ai_training : Permission
        Training or fine-tuning machine learning models on the work.
    modification : Permission
        Editing, processing, or adapting the work, including for private use.
    redistribution : Permission
        Making copies of the work available to third parties.
    modified_redistribution : Permission
        Making modified copies or adaptations available to third parties, which licenses such as CC BY-ND forbid even
        where they allow both modification and redistribution.
    network_service : Permission
        Letting third parties use software or a model that runs the work over a network.
    attribution : ObligationCondition | None
        When the source must be credited, or ``None`` when it never has to be.
    modification_notice : ObligationCondition | None
        When a modified work must state that it was modified, or ``None`` when it never has to.
    source_disclosure : ObligationCondition | None
        When the source form of the work must be made available, or ``None`` when it never has to be.
    downstream_terms : ObligationCondition | None
        When derived or combined works must be distributed on terms that keep rights or restrictions of the license,
        or ``None`` when they never have to be.
    share_alike : ObligationCondition | None
        When derived works must be released under the same license (copyleft), with its scope telling how far that
        reaches, or ``None`` when they may be under any license.

    Raises
    ------
    ValueError
        If modified redistribution is less restrictive than modification or redistribution, which it involves.
    """

    commercial_use: Permission
    non_research_use: Permission
    ai_training: Permission
    modification: Permission
    redistribution: Permission
    modified_redistribution: Permission
    network_service: Permission
    attribution: ObligationCondition | None
    modification_notice: ObligationCondition | None
    source_disclosure: ObligationCondition | None
    downstream_terms: ObligationCondition | None
    share_alike: ObligationCondition | None

    def __post_init__(self) -> None:
        involved: dict[str, Permission] = {"modification": self.modification, "redistribution": self.redistribution}
        for name, permission in involved.items():
            if permission.restrictiveness > self.modified_redistribution.restrictiveness:
                message: str = (
                    f"modified_redistribution must be as restrictive as {name} ({permission}), which it involves."
                )
                raise ValueError(message)

    @property
    def stated_kinds(self) -> tuple[UseKind | NarrowerUseKind, ...]:
        """
        Kinds of use these terms state a permission for item by item.

        Returns
        -------
        tuple[UseKind | NarrowerUseKind, ...]
            Every `UseKind`; subclasses add the narrower kinds they state.
        """
        return tuple(UseKind)

    def permission_for(self, kind: UseKind | NarrowerUseKind) -> Permission:
        """
        Whether these terms permit one kind of use.

        Parameters
        ----------
        kind : UseKind | NarrowerUseKind
            Kind of use.

        Returns
        -------
        Permission
            The permission the terms state for that kind, or for the kind it narrows when they state none for it.
        """
        if not isinstance(kind, UseKind):
            return self.permission_for(kind.broader)
        match kind:
            case UseKind.COMMERCIAL_USE:
                return self.commercial_use
            case UseKind.NON_RESEARCH_USE:
                return self.non_research_use
            case UseKind.AI_TRAINING:
                return self.ai_training
            case UseKind.MODIFICATION:
                return self.modification
            case UseKind.REDISTRIBUTION:
                return self.redistribution
            case UseKind.MODIFIED_REDISTRIBUTION:
                return self.modified_redistribution
            case UseKind.NETWORK_SERVICE:
                return self.network_service

    def condition_for(self, obligation: Obligation) -> ObligationCondition | None:
        """
        When these terms impose an obligation.

        Parameters
        ----------
        obligation : Obligation
            Duty in question.

        Returns
        -------
        ObligationCondition | None
            The condition the terms state for it, or ``None`` when they never impose it.
        """
        match obligation:
            case Obligation.ATTRIBUTION:
                return self.attribution
            case Obligation.MODIFICATION_NOTICE:
                return self.modification_notice
            case Obligation.SOURCE_DISCLOSURE:
                return self.source_disclosure
            case Obligation.DOWNSTREAM_TERMS:
                return self.downstream_terms
            case Obligation.SHARE_ALIKE:
                return self.share_alike

    @property
    def is_permissive(self) -> bool:
        """
        Whether the work may be used in any way, including in closed-source commercial products.

        Returns
        -------
        bool
            True when every stated kind of use is ``ALLOWED`` and nothing ever binds the user's own work: no source
            disclosure, downstream terms, or share-alike. Attribution and notices may still be required.
        """
        return (
            self.share_alike is None
            and self.source_disclosure is None
            and self.downstream_terms is None
            and all(self.permission_for(kind) is Permission.ALLOWED for kind in self.stated_kinds)
        )
