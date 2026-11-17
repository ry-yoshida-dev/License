from enum import Enum
from functools import cache

from .definition import LicenseDefinition
from .obligation_condition import ObligationCondition
from .obligation_trigger import ObligationTrigger
from .permission import Permission
from .terms import LicenseTerms
from .work_scope import WorkScope


class License(Enum):
    """
    Well-known license that a work, such as code, model weights, or a dataset, is distributed under.

    Values are SPDX license identifiers, or ``LicenseRef-`` identifiers for licenses SPDX does not list, so that
    ``License("MIT")`` looks a member up. `definition` gives the title, the short title, the URL of the license text,
    and the terms; titles are SPDX full names where SPDX lists the license, and short titles the names licensors and
    users abbreviate them to.

    Attributes
    ----------
    MIT
        MIT License.
    BSD_2_CLAUSE
        BSD 2-Clause License.
    BSD_3_CLAUSE
        BSD 3-Clause License, which also forbids using the contributors' names to endorse derived products.
    APACHE_2_0
        Apache License 2.0.
    MPL_2_0
        Mozilla Public License 2.0, whose copyleft covers only the modified files.
    LGPL_2_1_ONLY
        GNU Lesser General Public License v2.1 only. A program linked with the library is not brought under it, but
        is distributed on terms that let users modify and relink the library.
    LGPL_2_1_OR_LATER
        GNU Lesser General Public License v2.1 or any later version.
    LGPL_3_0_ONLY
        GNU Lesser General Public License v3.0 only, with the same downstream terms as v2.1.
    LGPL_3_0_OR_LATER
        GNU Lesser General Public License v3.0 or any later version.
    GPL_2_0_ONLY
        GNU General Public License v2.0 only.
    GPL_2_0_OR_LATER
        GNU General Public License v2.0 or any later version.
    GPL_3_0_ONLY
        GNU General Public License v3.0 only.
    GPL_3_0_OR_LATER
        GNU General Public License v3.0 or any later version.
    AGPL_3_0_ONLY
        GNU Affero General Public License v3.0 only, which extends copyleft to modified versions offered over a
        network. Serving an unmodified copy combined into a larger program is conservatively treated like serving a
        modified version.
    AGPL_3_0_OR_LATER
        GNU Affero General Public License v3.0 or any later version.
    CC0_1_0
        Creative Commons Zero v1.0 Universal, a public domain dedication.
    CC_BY_4_0
        Creative Commons Attribution 4.0 International.
    CC_BY_SA_4_0
        Creative Commons Attribution-ShareAlike 4.0 International.
    CC_BY_ND_4_0
        Creative Commons Attribution-NoDerivatives 4.0 International, which allows private adaptations but not
        sharing them. Whether a model trained on the work is an adaptation depends on the facts and jurisdiction.
    CC_BY_NC_4_0
        Creative Commons Attribution-NonCommercial 4.0 International.
    CC_BY_NC_SA_4_0
        Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
    CC_BY_NC_ND_4_0
        Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International.
    ODBL_1_0
        Open Data Commons Open Database License v1.0, used by OpenStreetMap. A database modified, or merged with other
        contents into a new one, is a derivative database; publicly using it, including serving works produced from
        it, brings it under the license and requires offering it.
    PUBLIC_DATA_LICENSE_1_0
        Public Data License (Version 1.0) (公共データ利用規約 第1.0版) of the Japanese Digital Agency, for public data
        of national and local governments. Its own terms ask for credit on any use, but content of national and
        local governments may be used under CC BY 4.0 instead, and the terms record that option. Content of other
        public bodies, or terms that adopters change in an accompanying notice, need a `LicenseDefinition` of their
        own.
    APPLE_MACHINE_LEARNING_RESEARCH_MODEL
        Apple Machine Learning Research Model License Agreement (``apple-amlr`` on Hugging Face), for non-commercial
        research only. Derived models, including fine-tuned ones, stay limited to research and are redistributed with
        the agreement. The license is personal and silent on hosting a model for others, which needs confirming.
        Each model ships its own copy of the text, so it has no canonical URL.
    """

    MIT = "MIT"
    BSD_2_CLAUSE = "BSD-2-Clause"
    BSD_3_CLAUSE = "BSD-3-Clause"
    APACHE_2_0 = "Apache-2.0"
    MPL_2_0 = "MPL-2.0"
    LGPL_2_1_ONLY = "LGPL-2.1-only"
    LGPL_2_1_OR_LATER = "LGPL-2.1-or-later"
    LGPL_3_0_ONLY = "LGPL-3.0-only"
    LGPL_3_0_OR_LATER = "LGPL-3.0-or-later"
    GPL_2_0_ONLY = "GPL-2.0-only"
    GPL_2_0_OR_LATER = "GPL-2.0-or-later"
    GPL_3_0_ONLY = "GPL-3.0-only"
    GPL_3_0_OR_LATER = "GPL-3.0-or-later"
    AGPL_3_0_ONLY = "AGPL-3.0-only"
    AGPL_3_0_OR_LATER = "AGPL-3.0-or-later"
    CC0_1_0 = "CC0-1.0"
    CC_BY_4_0 = "CC-BY-4.0"
    CC_BY_SA_4_0 = "CC-BY-SA-4.0"
    CC_BY_ND_4_0 = "CC-BY-ND-4.0"
    CC_BY_NC_4_0 = "CC-BY-NC-4.0"
    CC_BY_NC_SA_4_0 = "CC-BY-NC-SA-4.0"
    CC_BY_NC_ND_4_0 = "CC-BY-NC-ND-4.0"
    ODBL_1_0 = "ODbL-1.0"
    PUBLIC_DATA_LICENSE_1_0 = "LicenseRef-PDL-1.0"
    APPLE_MACHINE_LEARNING_RESEARCH_MODEL = "LicenseRef-Apple-AMLR"

    @property
    def definition(self) -> LicenseDefinition:
        """
        Title, URL of the license text, and terms of the license.

        Returns
        -------
        LicenseDefinition
            Definition whose identifier is the value of this member, built once and shared.
        """
        return _definition(self)


_LGPL_2_1_URL: str = "https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html"
_LGPL_3_0_URL: str = "https://www.gnu.org/licenses/lgpl-3.0.html"
_GPL_2_0_URL: str = "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html"
_GPL_3_0_URL: str = "https://www.gnu.org/licenses/gpl-3.0.html"
_AGPL_3_0_URL: str = "https://www.gnu.org/licenses/agpl-3.0.html"

# Each preset spells out every item, so that it can be checked against the license texts line by line.
_PUBLIC_DOMAIN: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=None,
    modification_notice=None,
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
_NOTICE: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=None,
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
_NOTICE_AND_CHANGES: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
_FILE_COPYLEFT: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=None,
    source_disclosure=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    downstream_terms=None,
    share_alike=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_FILES),
)
_LIBRARY_COPYLEFT: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    downstream_terms=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.COMBINED_WORK),
    share_alike=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
)
_STRONG_COPYLEFT: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    downstream_terms=None,
    share_alike=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.COMBINED_WORK),
)
_NETWORK_COPYLEFT: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=ObligationCondition(
        trigger=ObligationTrigger.REDISTRIBUTION_OR_MODIFIED_NETWORK_SERVICE, scope=WorkScope.ANY_FORM
    ),
    downstream_terms=None,
    share_alike=ObligationCondition(
        trigger=ObligationTrigger.REDISTRIBUTION_OR_MODIFIED_NETWORK_SERVICE, scope=WorkScope.COMBINED_WORK
    ),
)
_SHARE_ALIKE: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=None,
    share_alike=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
)
_NO_DERIVATIVES: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.PROHIBITED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
_NON_COMMERCIAL: LicenseTerms = LicenseTerms(
    commercial_use=Permission.PROHIBITED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
_NON_COMMERCIAL_SHARE_ALIKE: LicenseTerms = LicenseTerms(
    commercial_use=Permission.PROHIBITED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=None,
    share_alike=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
)
_NON_COMMERCIAL_NO_DERIVATIVES: LicenseTerms = LicenseTerms(
    commercial_use=Permission.PROHIBITED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.PROHIBITED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=None,
    share_alike=None,
)
_DATABASE_SHARE_ALIKE: LicenseTerms = LicenseTerms(
    commercial_use=Permission.ALLOWED,
    non_research_use=Permission.ALLOWED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.ALLOWED,
    attribution=ObligationCondition(
        trigger=ObligationTrigger.REDISTRIBUTION_OR_NETWORK_SERVICE, scope=WorkScope.ANY_FORM
    ),
    modification_notice=None,
    source_disclosure=ObligationCondition(
        trigger=ObligationTrigger.REDISTRIBUTION_OR_NETWORK_SERVICE, scope=WorkScope.COMBINED_WORK
    ),
    downstream_terms=None,
    share_alike=ObligationCondition(
        trigger=ObligationTrigger.REDISTRIBUTION_OR_NETWORK_SERVICE, scope=WorkScope.COMBINED_WORK
    ),
)
_RESEARCH_ONLY: LicenseTerms = LicenseTerms(
    commercial_use=Permission.PROHIBITED,
    non_research_use=Permission.PROHIBITED,
    ai_training=Permission.ALLOWED,
    modification=Permission.ALLOWED,
    redistribution=Permission.ALLOWED,
    modified_redistribution=Permission.ALLOWED,
    network_service=Permission.UNSPECIFIED,
    attribution=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.ANY_FORM),
    modification_notice=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    source_disclosure=None,
    downstream_terms=ObligationCondition(trigger=ObligationTrigger.REDISTRIBUTION, scope=WorkScope.MODIFIED_WORK),
    share_alike=None,
)


@cache
def _definition(member: License) -> LicenseDefinition:
    match member:
        case License.MIT:
            return _define(member, "MIT", "MIT License", "https://opensource.org/license/mit", _NOTICE)
        case License.BSD_2_CLAUSE:
            return _define(
                member,
                "BSD 2-Clause",
                'BSD 2-Clause "Simplified" License',
                "https://opensource.org/license/bsd-2-clause",
                _NOTICE,
            )
        case License.BSD_3_CLAUSE:
            return _define(
                member,
                "BSD 3-Clause",
                'BSD 3-Clause "New" or "Revised" License',
                "https://opensource.org/license/bsd-3-clause",
                _NOTICE,
            )
        case License.APACHE_2_0:
            return _define(
                member,
                "Apache 2.0",
                "Apache License 2.0",
                "https://www.apache.org/licenses/LICENSE-2.0",
                _NOTICE_AND_CHANGES,
            )
        case License.MPL_2_0:
            return _define(
                member,
                "MPL 2.0",
                "Mozilla Public License 2.0",
                "https://www.mozilla.org/en-US/MPL/2.0/",
                _FILE_COPYLEFT,
            )
        case License.LGPL_2_1_ONLY:
            return _define(
                member, "LGPLv2.1", "GNU Lesser General Public License v2.1 only", _LGPL_2_1_URL, _LIBRARY_COPYLEFT
            )
        case License.LGPL_2_1_OR_LATER:
            return _define(
                member, "LGPLv2.1+", "GNU Lesser General Public License v2.1 or later", _LGPL_2_1_URL, _LIBRARY_COPYLEFT
            )
        case License.LGPL_3_0_ONLY:
            return _define(
                member, "LGPLv3", "GNU Lesser General Public License v3.0 only", _LGPL_3_0_URL, _LIBRARY_COPYLEFT
            )
        case License.LGPL_3_0_OR_LATER:
            return _define(
                member, "LGPLv3+", "GNU Lesser General Public License v3.0 or later", _LGPL_3_0_URL, _LIBRARY_COPYLEFT
            )
        case License.GPL_2_0_ONLY:
            return _define(member, "GPLv2", "GNU General Public License v2.0 only", _GPL_2_0_URL, _STRONG_COPYLEFT)
        case License.GPL_2_0_OR_LATER:
            return _define(member, "GPLv2+", "GNU General Public License v2.0 or later", _GPL_2_0_URL, _STRONG_COPYLEFT)
        case License.GPL_3_0_ONLY:
            return _define(member, "GPLv3", "GNU General Public License v3.0 only", _GPL_3_0_URL, _STRONG_COPYLEFT)
        case License.GPL_3_0_OR_LATER:
            return _define(member, "GPLv3+", "GNU General Public License v3.0 or later", _GPL_3_0_URL, _STRONG_COPYLEFT)
        case License.AGPL_3_0_ONLY:
            return _define(
                member, "AGPLv3", "GNU Affero General Public License v3.0 only", _AGPL_3_0_URL, _NETWORK_COPYLEFT
            )
        case License.AGPL_3_0_OR_LATER:
            return _define(
                member, "AGPLv3+", "GNU Affero General Public License v3.0 or later", _AGPL_3_0_URL, _NETWORK_COPYLEFT
            )
        case License.CC0_1_0:
            return _define(
                member,
                "CC0 1.0",
                "Creative Commons Zero v1.0 Universal",
                "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
                _PUBLIC_DOMAIN,
            )
        case License.CC_BY_4_0:
            return _define(
                member,
                "CC BY 4.0",
                "Creative Commons Attribution 4.0 International",
                "https://creativecommons.org/licenses/by/4.0/legalcode",
                _NOTICE_AND_CHANGES,
            )
        case License.CC_BY_SA_4_0:
            return _define(
                member,
                "CC BY-SA 4.0",
                "Creative Commons Attribution Share Alike 4.0 International",
                "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
                _SHARE_ALIKE,
            )
        case License.CC_BY_ND_4_0:
            return _define(
                member,
                "CC BY-ND 4.0",
                "Creative Commons Attribution No Derivatives 4.0 International",
                "https://creativecommons.org/licenses/by-nd/4.0/legalcode",
                _NO_DERIVATIVES,
            )
        case License.CC_BY_NC_4_0:
            return _define(
                member,
                "CC BY-NC 4.0",
                "Creative Commons Attribution Non Commercial 4.0 International",
                "https://creativecommons.org/licenses/by-nc/4.0/legalcode",
                _NON_COMMERCIAL,
            )
        case License.CC_BY_NC_SA_4_0:
            return _define(
                member,
                "CC BY-NC-SA 4.0",
                "Creative Commons Attribution Non Commercial Share Alike 4.0 International",
                "https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode",
                _NON_COMMERCIAL_SHARE_ALIKE,
            )
        case License.CC_BY_NC_ND_4_0:
            return _define(
                member,
                "CC BY-NC-ND 4.0",
                "Creative Commons Attribution Non Commercial No Derivatives 4.0 International",
                "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
                _NON_COMMERCIAL_NO_DERIVATIVES,
            )
        case License.ODBL_1_0:
            return _define(
                member,
                "ODbL 1.0",
                "Open Data Commons Open Database License v1.0",
                "https://opendatacommons.org/licenses/odbl/1-0/",
                _DATABASE_SHARE_ALIKE,
            )
        case License.PUBLIC_DATA_LICENSE_1_0:
            return _define(
                member,
                "PDL 1.0",
                "Public Data License (Version 1.0)",
                "https://www.digital.go.jp/resources/open_data/public_data_license_v1.0",
                _NOTICE_AND_CHANGES,
            )
        case License.APPLE_MACHINE_LEARNING_RESEARCH_MODEL:
            return _define(
                member,
                "Apple ML Research Model",
                "Apple Machine Learning Research Model License Agreement",
                None,
                _RESEARCH_ONLY,
            )


def _define(member: License, short_title: str, title: str, url: str | None, terms: LicenseTerms) -> LicenseDefinition:
    return LicenseDefinition(title=title, short_title=short_title, terms=terms, identifier=member.value, url=url)
