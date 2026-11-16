from enum import Enum


class Permission(Enum):
    """
    Whether a license permits one kind of use of a work.

    Attributes
    ----------
    ALLOWED
        The use is permitted, subject only to the obligations the license attaches to it.
    CONDITIONAL
        The use is permitted only under further conditions stated in the license text, such as prior approval.
    UNSPECIFIED
        Whether the use is permitted is not settled by the terms, so it must be confirmed with the rights holder or
        against the license texts.
    PROHIBITED
        The use is not permitted.
    """

    ALLOWED = "allowed"
    CONDITIONAL = "conditional"
    UNSPECIFIED = "unspecified"
    PROHIBITED = "prohibited"

    @property
    def restrictiveness(self) -> int:
        """
        Rank of the permission from the least restrictive.

        An unspecified use ranks above a conditional one because nothing tells how to satisfy it.

        Returns
        -------
        int
            0 for ``ALLOWED``, 1 for ``CONDITIONAL``, 2 for ``UNSPECIFIED``, and 3 for ``PROHIBITED``.
        """
        match self:
            case Permission.ALLOWED:
                return 0
            case Permission.CONDITIONAL:
                return 1
            case Permission.UNSPECIFIED:
                return 2
            case Permission.PROHIBITED:
                return 3

    def combine(self, other: "Permission") -> "Permission":
        """
        Permission of a use that needs both this and another permission.

        Parameters
        ----------
        other : Permission
            Permission of the other kind of use.

        Returns
        -------
        Permission
            The more restrictive of the two.
        """
        return other if other.restrictiveness > self.restrictiveness else self
