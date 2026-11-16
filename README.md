# license-kit

## Overview

`license_kit` defines the licenses that code, model weights, and datasets are distributed under by their terms, such as commercial use, redistribution, modification, and copyleft. Packages declare the licensing of their works as data, and applications assess an intended use against it to learn whether the use is permitted, which license restricts it, and which obligations, such as attribution or source disclosure, it brings into effect. The terms summarize each license; the license text remains authoritative. See [src/license_kit/README.md](src/license_kit/README.md) for the package contents.

Well-known licenses, by SPDX identifier, grouped by how far their copyleft reaches and whether they allow commercial use:

| Copyleft | Commercial use allowed | Commercial use prohibited |
| --- | --- | --- |
| None | `MIT`, `BSD-2-Clause`, `BSD-3-Clause`, `Apache-2.0`, `CC0-1.0`, `CC-BY-4.0`, `CC-BY-ND-4.0`, `LicenseRef-PDL-1.0` | `CC-BY-NC-4.0`, `CC-BY-NC-ND-4.0`, `LicenseRef-Apple-AMLR` |
| Modified files | `MPL-2.0` | |
| Modified work | `LGPL-2.1-only`, `LGPL-2.1-or-later`, `LGPL-3.0-only`, `LGPL-3.0-or-later`, `CC-BY-SA-4.0` | `CC-BY-NC-SA-4.0` |
| Combined work | `GPL-2.0-only`, `GPL-2.0-or-later`, `GPL-3.0-only`, `GPL-3.0-or-later`, `AGPL-3.0-only`, `AGPL-3.0-or-later`, `ODbL-1.0` | |

Works under several licenses are described with `LicenseChoice` (SPDX `OR`) and `LicenseCombination` (SPDX `AND`), which nest.

## Installation

```bash
pip install git+https://github.com/ry-yoshida-dev/License
```

## Usage

```python
from license_kit import (
    IntendedUse,
    License,
    LicenseChoice,
    LicenseCombination,
    LicenseDefinition,
    LicenseTerms,
    ObligationCondition,
    ObligationTrigger,
    Permission,
    UseAssessment,
    WorkScope,
)

# A commercial web service built on a modified AGPL library.
use = IntendedUse(
    is_commercial=True,
    is_research_only=False,
    is_used_for_ai_training=False,
    is_modified=True,
    is_combined=True,
    is_redistributed=False,
    is_offered_over_network=True,
)
assessment = UseAssessment.of(License.AGPL_3_0_ONLY.definition, use)
print(assessment.permission)  # Permission.ALLOWED
obligations = {requirement.obligation for requirement in assessment.requirements}
print(sorted(obligation.value for obligation in obligations))  # ['share_alike', 'source_disclosure']

# Terms that match no well-known license are defined item by item.
dataset_license = LicenseDefinition(
    title="Terms of a municipal dataset",
    identifier="LicenseRef-Municipal-Data",
    url="https://example.com/terms",
    terms=LicenseTerms(
        commercial_use=Permission.PROHIBITED,
        non_research_use=Permission.ALLOWED,
        ai_training=Permission.UNSPECIFIED,
        modification=Permission.ALLOWED,
        redistribution=Permission.ALLOWED,
        modified_redistribution=Permission.ALLOWED,
        network_service=Permission.ALLOWED,
        attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
        modification_notice=None,
        source_disclosure=None,
        downstream_terms=None,
        share_alike=None,
    ),
)

# A package bundling MIT code with the dataset must comply with both.
package = LicenseCombination(parts=(License.MIT.definition, dataset_license))
(restriction,) = UseAssessment.of(package, use).restrictions
print(restriction.license.title)  # Terms of a municipal dataset
print(restriction.kind, restriction.permission)  # UseKind.COMMERCIAL_USE Permission.PROHIBITED

# A dual-licensed work is assessed under the option that constrains the use least.
choice = LicenseChoice(options=(License.CC_BY_NC_4_0.definition, License.MIT.definition))
print([license.title for license in UseAssessment.of(choice, use).licenses])  # ['MIT License']
```
