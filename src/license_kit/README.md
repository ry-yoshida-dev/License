# license_kit

## Overview

Licenses that code, model weights, and datasets are distributed under, each defined item by item by the permissions it grants and the obligations it attaches. Well-known licenses are `License` members; works under conditions of their own are described by a `LicenseDefinition` directly. `UseAssessment.of` assesses an `IntendedUse` against any licensing, including SPDX `OR` and `AND` expressions, into the restrictions and requirements of the alternative that constrains it least.

## Components

| Component | Description |
| --- | --- |
| [license.py](./license.py) | `License` enumerates well-known licenses by SPDX identifier and gives the definition of each. |
| [expression.py](./expression.py) | `LicenseExpression` is the protocol of any licensing, a license, a choice, or a combination, expanded into the alternative sets of licenses that comply with it. |
| [definition.py](./definition.py) | `LicenseDefinition` names a license, links its text, and holds its terms. |
| [choice.py](./choice.py) | `LicenseChoice` offers licensings to choose from (SPDX `OR`). |
| [combination.py](./combination.py) | `LicenseCombination` applies licensings together (SPDX `AND`). |
| [terms.py](./terms.py) | `LicenseTerms` lists the permission for each kind of use and the condition of each obligation. |
| [intended_use.py](./intended_use.py) | `IntendedUse` states, item by item, how a work is going to be used. |
| [use_kind.py](./use_kind.py) | `UseKind` names the kinds of use a license permits or restricts, such as commercial use. |
| [permission.py](./permission.py) | `Permission` states whether one kind of use is allowed, conditional, unspecified, or prohibited. |
| [obligation.py](./obligation.py) | `Obligation` names a duty a license attaches to a use, such as attribution or source disclosure. |
| [obligation_condition.py](./obligation_condition.py) | `ObligationCondition` states when an obligation comes into effect: its trigger and the works it concerns. |
| [obligation_trigger.py](./obligation_trigger.py) | `ObligationTrigger` states which kind of use brings an obligation into effect. |
| [work_scope.py](./work_scope.py) | `WorkScope` states which forms of the work an obligation concerns: any form, modified files, the modified work, or any combined work. |
| [use_assessment.py](./use_assessment.py) | `UseAssessment` assesses a use against a licensing: the licenses applied, restrictions, requirements, conflicting licenses, and the resulting permission. |
| [restriction.py](./restriction.py) | `Restriction` records a kind of use that a license does not plainly allow. |
| [requirement.py](./requirement.py) | `Requirement` records an obligation that a use brings into effect under a license. |
| [py.typed](./py.typed) | Marks the package as typed (PEP 561). |
