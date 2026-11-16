from enum import Enum

from .intended_use import IntendedUse


class ObligationTrigger(Enum):
    """
    Kind of use that brings an obligation of a license into effect.

    Attributes
    ----------
    ANY_USE
        Every use, including private use of the work as is.
    REDISTRIBUTION
        Making copies of the work available to third parties.
    REDISTRIBUTION_OR_NETWORK_SERVICE
        Making copies available, or letting third parties use the work over a network.
    REDISTRIBUTION_OR_MODIFIED_NETWORK_SERVICE
        Making copies available, or letting third parties use a modified or combined version over a network, as
        section 13 of the AGPL requires.
    """

    ANY_USE = "any_use"
    REDISTRIBUTION = "redistribution"
    REDISTRIBUTION_OR_NETWORK_SERVICE = "redistribution_or_network_service"
    REDISTRIBUTION_OR_MODIFIED_NETWORK_SERVICE = "redistribution_or_modified_network_service"

    def is_triggered_by(self, use: IntendedUse) -> bool:
        """
        Whether an intended use brings the obligation into effect.

        Parameters
        ----------
        use : IntendedUse
            How the work is going to be used.

        Returns
        -------
        bool
            True when the use is of this kind.
        """
        match self:
            case ObligationTrigger.ANY_USE:
                return True
            case ObligationTrigger.REDISTRIBUTION:
                return use.is_redistributed
            case ObligationTrigger.REDISTRIBUTION_OR_NETWORK_SERVICE:
                return use.is_redistributed or use.is_offered_over_network
            case ObligationTrigger.REDISTRIBUTION_OR_MODIFIED_NETWORK_SERVICE:
                return use.is_redistributed or (use.is_offered_over_network and (use.is_modified or use.is_combined))
