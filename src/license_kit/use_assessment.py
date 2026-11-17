from dataclasses import dataclass
from typing import Self

from .definition import LicenseDefinition
from .expression import LicenseExpression
from .intended_use import IntendedUse
from .obligation import Obligation
from .permission import Permission
from .requirement import Requirement
from .restriction import Restriction
from .terms import LicenseTerms
from .work_scope import WorkScope


@dataclass(frozen=True, kw_only=True)
class UseAssessment:
    """
    Whether an intended use of a work is permitted, why not, and what its licenses require of it.

    Attributes
    ----------
    licenses : frozenset[LicenseDefinition]
        Licenses that apply to the use, which for a choice are those of the option chosen.
    restrictions : frozenset[Restriction]
        Kinds of use involved that a license does not plainly allow.
    requirements : frozenset[Requirement]
        Obligations the use brings into effect, to be fulfilled if it goes ahead, even when it is not permitted.
    conflicts : frozenset[LicenseDefinition]
        Licenses whose terms may not be met together, or an empty set when they can: several licenses that each
        require the work to be released under them, or a copyleft over a work that takes in the other material, such
        as a GPL program or an adaptation under CC BY-SA mixed with other material, together with a license that adds
        restrictions. Whether they are compatible after all, as the LGPL is with the GPL or the GPL-3.0 with the
        AGPL-3.0, must be confirmed against their texts; incompatibilities between a copyleft and a permissive
        license, such as GPL-2.0 with Apache-2.0, are not detected.
    """

    licenses: frozenset[LicenseDefinition]
    restrictions: frozenset[Restriction]
    requirements: frozenset[Requirement]
    conflicts: frozenset[LicenseDefinition]

    @classmethod
    def of(cls, expression: LicenseExpression, use: IntendedUse) -> Self:
        """
        Assess an intended use against a licensing, choosing the alternative that constrains it least.

        Parameters
        ----------
        expression : LicenseExpression
            Licensing of the work: a license, a choice, or a combination.
        use : IntendedUse
            How the work is going to be used.

        Returns
        -------
        UseAssessment
            Assessment under the alternative with the least restrictive permission and, among those, the lightest
            obligations, weighed by severity and then by how far each reaches, where a set of obligations contained
            in another is lighter; the earliest alternative wins a tie. It is returned even when no alternative
            permits the use.
        """
        return min(
            (cls._of_licenses(licenses, use) for licenses in expression.alternatives),
            key=lambda assessment: assessment._burden,
        )

    @classmethod
    def _of_licenses(cls, licenses: frozenset[LicenseDefinition], use: IntendedUse) -> Self:
        restrictions: frozenset[Restriction] = frozenset(
            Restriction(license=license_, kind=kind, permission=permission)
            for license_ in licenses
            for kind in use.involved_kinds
            if (permission := license_.terms.permission_for(kind)) is not Permission.ALLOWED
        )
        requirements: frozenset[Requirement] = frozenset(
            Requirement(license=license_, obligation=obligation, condition=condition)
            for license_ in licenses
            for obligation in Obligation
            if (condition := license_.terms.condition_for(obligation)) is not None and condition.applies_to(use)
        )
        # Copyleft limited to the modified files, as in the MPL, lets those files sit in a work under another license.
        copyleft: list[Requirement] = [
            requirement
            for requirement in requirements
            if requirement.obligation is Obligation.SHARE_ALIKE
            and requirement.condition.scope is not WorkScope.MODIFIED_FILES
        ]
        conflicting: set[LicenseDefinition] = {requirement.license for requirement in copyleft}
        # Copyleft over a work that takes in the other material, as in the GPL or in an adaptation under CC BY-SA,
        # forbids further restrictions by the other licenses.
        if any(_takes_in_other_material(requirement.condition.scope, use) for requirement in copyleft):
            conflicting |= {license_ for license_ in licenses if _is_restricting_further(license_)}
        return cls(
            licenses=licenses,
            restrictions=restrictions,
            requirements=requirements,
            conflicts=frozenset(conflicting) if len(conflicting) > 1 else frozenset(),
        )

    @property
    def permission(self) -> Permission:
        """
        Whether the use may go ahead.

        Returns
        -------
        Permission
            The most restrictive permission among the restrictions, or ``ALLOWED`` when there are none; at least
            ``UNSPECIFIED`` when licenses conflict.
        """
        permission: Permission = Permission.UNSPECIFIED if self.conflicts else Permission.ALLOWED
        for restriction in self.restrictions:
            permission = permission.combine(restriction.permission)
        return permission

    @property
    def _burden(self) -> tuple[int, tuple[tuple[int, int], ...]]:
        # Sorting weights from the heaviest makes a set of obligations rank below any superset of it.
        weights: list[tuple[int, int]] = sorted(
            (
                (requirement.obligation.severity, requirement.condition.scope.breadth)
                for requirement in self.requirements
            ),
            reverse=True,
        )
        return self.permission.restrictiveness, tuple(weights)


def _takes_in_other_material(scope: WorkScope, use: IntendedUse) -> bool:
    match scope:
        case WorkScope.COMBINED_WORK | WorkScope.ANY_FORM:
            return True
        case WorkScope.MODIFIED_WORK:
            return use.is_modified and use.is_combined
        case WorkScope.MODIFIED_FILES:
            return False


def _is_restricting_further(license_: LicenseDefinition) -> bool:
    terms: LicenseTerms = license_.terms
    is_copyleft_beyond_files: bool = (
        terms.share_alike is not None and terms.share_alike.scope is not WorkScope.MODIFIED_FILES
    )
    return (
        is_copyleft_beyond_files
        or terms.downstream_terms is not None
        or any(terms.permission_for(kind) is not Permission.ALLOWED for kind in terms.stated_kinds)
    )
