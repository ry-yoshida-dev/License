from enum import Enum

from .intended_use import IntendedUse


class WorkScope(Enum):
    """
    Forms of the licensed work that an obligation concerns, and so how far it reaches.

    Attributes
    ----------
    ANY_FORM
        The work as is as well as any work derived from it, as for attribution.
    MODIFIED_FILES
        Only the modified files of the work, as for the copyleft of the MPL; files added beside them are not concerned.
    MODIFIED_WORK
        Modifications and adaptations of the work, but not larger works it is merely combined with, as for the
        copyleft of the LGPL and CC BY-SA.
    COMBINED_WORK
        Modifications of the work and any larger work it is combined with, as for the copyleft of the GPL and AGPL, and
        of the ODbL, under which merging the contents into a new database makes a derivative database.
    """

    ANY_FORM = "any_form"
    MODIFIED_FILES = "modified_files"
    MODIFIED_WORK = "modified_work"
    COMBINED_WORK = "combined_work"

    @property
    def breadth(self) -> int:
        """
        Rank of how many forms of the work the scope reaches, from the narrowest.

        Returns
        -------
        int
            0 for ``MODIFIED_FILES``, 1 for ``MODIFIED_WORK``, 2 for ``COMBINED_WORK``, and 3 for ``ANY_FORM``.
        """
        match self:
            case WorkScope.MODIFIED_FILES:
                return 0
            case WorkScope.MODIFIED_WORK:
                return 1
            case WorkScope.COMBINED_WORK:
                return 2
            case WorkScope.ANY_FORM:
                return 3

    def covers(self, use: IntendedUse) -> bool:
        """
        Whether an intended use produces a work within this scope.

        Parameters
        ----------
        use : IntendedUse
            How the work is going to be used.

        Returns
        -------
        bool
            Always True for ``ANY_FORM``; otherwise True when the use modifies the work, or, for ``COMBINED_WORK``,
            also when it combines the work.
        """
        match self:
            case WorkScope.ANY_FORM:
                return True
            case WorkScope.MODIFIED_FILES | WorkScope.MODIFIED_WORK:
                return use.is_modified
            case WorkScope.COMBINED_WORK:
                return use.is_modified or use.is_combined
