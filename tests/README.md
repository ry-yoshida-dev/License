# tests

## Overview

Pytest suite for the `license_kit` package. Tests that need an intended use derive it from the `private_use` fixture.

## Components

| Component | Description |
| --- | --- |
| [conftest.py](./conftest.py) | `private_use` fixture: a non-commercial use of the work as is, not limited to research, shared with nobody. |
| [test_license.py](./test_license.py) | `TestLicense`: golden tables, written from the license texts, of every license under canonical uses such as shipping a modified copy, shipping a combined work, and serving over a network. |
| [test_definition.py](./test_definition.py) | `TestLicenseDefinition`: a license is its own only alternative, and blank titles, invalid identifiers, and non-HTTP URLs are refused. |
| [test_choice.py](./test_choice.py) | `TestLicenseChoice`: the option that constrains a use least is chosen, including among combinations. |
| [test_combination.py](./test_combination.py) | `TestLicenseCombination`: every part's restrictions and requirements apply, and a choice inside is resolved for the whole combination. |
| [test_terms.py](./test_terms.py) | `TestLicenseTerms`: each kind of use and obligation reads its item, permissiveness excludes source disclosure, downstream terms, and copyleft, and inconsistent terms are refused. |
| [test_intended_use.py](./test_intended_use.py) | `TestIntendedUse`: each item of a use involves its kind of use. |
| [test_narrower_use_kind.py](./test_narrower_use_kind.py) | `TestNarrowerUseKind`: a narrower kind stands in for the kinds it narrows, terms unaware of it answer for the broader kind, subclassed terms answer for it, and cycles or narrowing an uninvolved kind are refused. |
| [test_use_assessment.py](./test_use_assessment.py) | `TestUseAssessment`: restrictions and requirements are attributed to their license, copyleft of several licenses conflicts unless limited to modified files, and copyleft over a work that takes in other material conflicts with licenses adding restrictions. |
| [test_restriction.py](./test_restriction.py) | `TestRestriction`: an allowed kind of use is refused as a restriction. |
| [test_permission.py](./test_permission.py) | `TestPermission`: permissions rank by restrictiveness and combine into the more restrictive. |
| [test_obligation.py](./test_obligation.py) | `TestObligation`: obligations rank by severity, copyleft heaviest. |
| [test_obligation_trigger.py](./test_obligation_trigger.py) | `TestObligationTrigger`: each use brings exactly its triggers into effect. |
| [test_obligation_condition.py](./test_obligation_condition.py) | `TestObligationCondition`: a condition needs both its trigger and its scope. |
| [test_work_scope.py](./test_work_scope.py) | `TestWorkScope`: scopes rank by breadth, only any-form scope covers the work as is, every scope covers modification, and only the any-form and combined-work scopes cover combination. |
| [test_readme.py](./test_readme.py) | `TestReadme`: the root README's usage example prints what its comments say. |
