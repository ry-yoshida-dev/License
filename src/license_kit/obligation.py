from enum import Enum


class Obligation(Enum):
    """
    Duty that a license attaches to a use of a work.

    Attributes
    ----------
    ATTRIBUTION
        Credit the source, such as by keeping its copyright and license notices or by citing it.
    MODIFICATION_NOTICE
        State that the work was modified, and by whom where the license asks for it.
    SOURCE_DISCLOSURE
        Make the source form of the licensed work, as distributed or as offered over a network, available to its
        recipients or users: the source code of software, or a machine-readable copy of a database or its alterations.
        It covers the licensed work, not other works it is merely combined with.
    DOWNSTREAM_TERMS
        Distribute the derived or combined work on terms that keep rights or restrictions the license states, without
        releasing it under that license: for example, letting users relink a modified LGPL library, or passing on a
        research-only restriction.
    SHARE_ALIKE
        Release the modified or combined work under the same license (copyleft), including its source form, as the
        license requires. The scope of its `ObligationCondition` tells how far the duty reaches.
    """

    ATTRIBUTION = "attribution"
    MODIFICATION_NOTICE = "modification_notice"
    SOURCE_DISCLOSURE = "source_disclosure"
    DOWNSTREAM_TERMS = "downstream_terms"
    SHARE_ALIKE = "share_alike"

    @property
    def severity(self) -> int:
        """
        Rank of how much the duty constrains the user's own work, from the lightest.

        Returns
        -------
        int
            0 for ``ATTRIBUTION``, 1 for ``MODIFICATION_NOTICE``, 2 for ``SOURCE_DISCLOSURE``, 3 for
            ``DOWNSTREAM_TERMS``, and 4 for ``SHARE_ALIKE``.
        """
        match self:
            case Obligation.ATTRIBUTION:
                return 0
            case Obligation.MODIFICATION_NOTICE:
                return 1
            case Obligation.SOURCE_DISCLOSURE:
                return 2
            case Obligation.DOWNSTREAM_TERMS:
                return 3
            case Obligation.SHARE_ALIKE:
                return 4
