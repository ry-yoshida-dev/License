import re
from dataclasses import dataclass
from urllib.parse import ParseResult, urlparse

from .terms import LicenseTerms

_IDENTIFIER_PATTERN: re.Pattern[str] = re.compile(r"[A-Za-z0-9][A-Za-z0-9.\-]*")


@dataclass(frozen=True, kw_only=True)
class LicenseDefinition:
    """
    License a work is distributed under: its name, where its text is, and its terms item by item.

    Well-known licenses are obtained from `License` members; works under conditions of their own, such as datasets of
    a single publisher, are described by constructing one directly, with a ``LicenseRef-`` identifier if any rather
    than the identifier of a `License` member. So is a license with an exception that changes its terms, such as
    ``GPL-2.0-only WITH Classpath-exception-2.0``. The terms summarize the license; its text remains authoritative.

    Attributes
    ----------
    title : str
        Human-readable name of the license.
    short_title : str
        Short name of the license for lists and notices, such as ``CC BY 4.0``.
    terms : LicenseTerms
        Terms of the license, item by item.
    identifier : str | None
        SPDX license identifier, such as ``MIT`` or ``LicenseRef-Municipal-Data``, or ``None`` when the license has
        none.
    url : str | None
        HTTP or HTTPS page of the license text, or ``None`` when no canonical page exists.

    Raises
    ------
    ValueError
        If the title or the short title is blank, the identifier is not made of the characters SPDX allows, or the URL
        is not an absolute HTTP or HTTPS URL.
    """

    title: str
    short_title: str
    terms: LicenseTerms
    identifier: str | None
    url: str | None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be blank.")
        if not self.short_title.strip():
            raise ValueError("short_title must not be blank.")
        if self.identifier is not None and _IDENTIFIER_PATTERN.fullmatch(self.identifier) is None:
            raise ValueError(
                f"identifier must be letters, digits, '.', and '-', led by a letter or digit: {self.identifier!r}"
            )
        if self.url is not None:
            parsed: ParseResult = urlparse(self.url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(f"url must be an absolute HTTP or HTTPS URL: {self.url!r}")

    @property
    def alternatives(self) -> tuple[frozenset["LicenseDefinition"], ...]:
        """
        Every way the licensing can be complied with, so that a single license is a `LicenseExpression` too.

        Returns
        -------
        tuple[frozenset[LicenseDefinition], ...]
            This license alone.
        """
        return (frozenset({self}),)
