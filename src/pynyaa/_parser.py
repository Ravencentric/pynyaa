# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import datetime as dt
import re
from typing import TYPE_CHECKING
from urllib.parse import urljoin, urlsplit

import bs4

from ._enums import Category
from ._errors import UnexpectedContentError
from ._models import Submitter

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence


class SafeTag:
    """Wrapper around a `bs4.Tag` that guarantees non-None selector results."""

    __slots__ = ("_tag",)

    def __init__(self, tag: bs4.Tag) -> None:
        self._tag = tag

    def select_one(self, selector: str) -> SafeTag:
        tag = self._tag.select_one(selector)
        if tag is None:  # pragma: no cover
            msg = f"Missing expected child element: {selector!r}"
            raise UnexpectedContentError(msg)
        return SafeTag(tag)

    def get_text(self) -> str:
        return self._tag.get_text().strip()

    @property
    def attrs(self) -> dict[str, str]:
        return self._tag.attrs  # pyrefly: ignore[bad-return]


class SafeSoup:
    """`BeautifulSoup` wrapper that always returns `SafeTag`, raising UnexpectedContentError if missing."""

    __slots__ = ("_soup",)

    def __init__(self, html: str) -> None:
        self._soup = bs4.BeautifulSoup(html, "html.parser")

    def select_one(self, selector: str) -> SafeTag:
        tag = self._soup.select_one(selector)
        if tag is None:  # pragma: no cover
            msg = f"Missing expected element: {selector!r}"
            raise UnexpectedContentError(msg)
        return SafeTag(tag)

    def select(self, selector: str) -> Sequence[SafeTag]:
        return [SafeTag(tag) for tag in self._soup.select(selector)]


class TorrentPanelParser:
    """Parser for a torrent's metadata panel (title, category, size, etc.)."""

    __slots__ = ("_body", "_url")

    def __init__(self, *, body: SafeTag, url: str):
        self._body = body
        self._url = url

    def select_field(self, label: str) -> SafeTag:
        return self._body.select_one(f'.panel-body > .row > .col-md-1:-soup-contains-own("{label}") + .col-md-5')

    def title(self) -> str:
        return self._body.select_one(".panel-heading > .panel-title").get_text()

    def category(self) -> Category:
        category = self.select_field("Category:").get_text().strip()
        return Category(category)

    def datetime(self) -> dt.datetime:
        timestamp = self.select_field("Date:").attrs["data-timestamp"]
        return dt.datetime.fromtimestamp(int(timestamp), tz=dt.timezone.utc)

    def submitter(self) -> Submitter | None:
        submitter = self.select_field("Submitter:")
        name = submitter.get_text()

        if name == "Anonymous":
            return None

        url = urljoin(self._url, f"/user/{name}")
        title = submitter.select_one("a").attrs["title"].lower()
        is_trusted = "trusted" in title
        is_banned = "banned" in title

        return Submitter(name=name, url=url, is_trusted=is_trusted, is_banned=is_banned)

    def seeders(self) -> int:
        return int(self.select_field("Seeders:").get_text())

    def leechers(self) -> int:
        return int(self.select_field("Leechers:").get_text())

    def completed(self) -> int:
        return int(self.select_field("Completed:").get_text())

    def information(self) -> str | None:
        information = self.select_field("Information:").get_text().strip()
        if information == "No information.":
            return None
        return information

    def infohash(self) -> str:
        selector = '.panel-body > .row > .col-md-offset-6.col-md-1:-soup-contains-own("Info hash:") + .col-md-5'
        return self._body.select_one(selector).get_text()

    def magnet(self) -> str:
        return self._body.select_one('.panel-footer.clearfix > a[href^="magnet:"]').attrs["href"]


class TorrentPageParser:
    """Parser for a full torrent details page, including description and status."""

    __slots__ = ("_body", "_soup", "_url")

    def __init__(self, *, html: str, url: str) -> None:
        self._soup = SafeSoup(html)
        self._body = self._soup.select_one("div:is(.panel.panel-default, .panel.panel-success, .panel.panel-danger)")
        self._url = url

    @property
    def panel(self) -> TorrentPanelParser:
        return TorrentPanelParser(body=self._body, url=self._url)

    def is_trusted(self) -> bool:
        return "panel-success" in self._body.attrs["class"]

    def is_remake(self) -> bool:
        return "panel-danger" in self._body.attrs["class"]

    def description(self) -> str | None:
        description = self._soup.select_one("#torrent-description").get_text()
        if description == "#### No description.":
            return None
        return description


class SearchPageParser:
    """Parser for search result pages, yielding torrent IDs and pagination info."""

    __slots__ = ("_html", "_soup")

    def __init__(self, html: str) -> None:
        self._html = html
        self._soup = SafeSoup(html)

    def pages(self) -> Iterator[int]:
        if pages := self._soup.select("ul.pagination > li:not(.next) > a[href]"):
            last = int(pages[-1].get_text()) + 1
            yield from range(2, last)

    def results(self) -> Iterator[int]:
        for id in re.findall(r"<a href=\"(?:/view/(\d+))\" title=\".*\">.*</a>", self._html):
            yield int(id)


def parse_release_id(page: int | str, /) -> int:
    """Extract a release ID from an integer or release URL."""
    match page:
        case int():
            return page
        case str():
            url = urlsplit(page)
            _, _, id = url.path.rstrip("/").rpartition("/")
            if url.netloc and id.isdecimal():
                return int(id)
            msg = f"Invalid format for 'page'. Expected a valid URL or numeric ID, but got {page!r}."
            raise ValueError(msg)
        case _:
            msg = f"Parameter 'page' expected 'int' or 'str', but got {type(page).__name__!r}."
            raise TypeError(msg)
