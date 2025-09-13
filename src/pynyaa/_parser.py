from __future__ import annotations

import datetime as dt
import math
import re
from typing import TYPE_CHECKING, NewType
from urllib.parse import unquote, urljoin

import bs4

from ._enums import Category
from ._errors import ParsingError
from ._models import Submitter

if TYPE_CHECKING:
    from collections.abc import Iterator

TorrentID = NewType("TorrentID", int)
PageNumber = NewType("PageNumber", int)


class SafeTag:
    """Wrapper around a `bs4.Tag` that guarantees non-None selector results."""

    __slots__ = ("_tag",)

    def __init__(self, tag: bs4.Tag) -> None:
        self._tag = tag

    def select_one(self, selector: str) -> SafeTag:
        tag = self._tag.select_one(selector)
        if tag is None:  # pragma: no cover
            msg = f"Missing expected child element: {selector!r}"
            raise ParsingError(msg)
        return SafeTag(tag)

    def get_text(self) -> str:
        return self._tag.get_text().strip()

    @property
    def attrs(self) -> dict[str, str]:
        return self._tag.attrs  # type: ignore[return-value]


class SafeSoup:
    """`BeautifulSoup` wrapper that always returns `SafeTag`, raising ParsingError if missing."""

    __slots__ = ("_soup",)

    def __init__(self, html: str) -> None:
        self._soup = bs4.BeautifulSoup(html, "html.parser")

    def select_one(self, selector: str) -> SafeTag:
        tag = self._soup.select_one(selector)
        if tag is None:  # pragma: no cover
            msg = f"Missing expected element: {selector!r}"
            raise ParsingError(msg)
        return SafeTag(tag)

    def select(self, selector: str) -> Iterator[SafeTag]:
        for tag in self._soup.select(selector):
            yield SafeTag(tag)


class TorrentPanelParser:
    """Parser for a torrent's metadata panel (title, category, size, etc.)."""

    __slots__ = ("_base_url", "_body")

    def __init__(self, *, body: SafeTag, base_url: str):
        self._body = body
        self._base_url = base_url

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

        url = urljoin(self._base_url, f"/user/{name}")
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

    def size(self) -> int:
        value, unit = self.select_field("File size:").get_text().split(" ", maxsplit=1)

        match unit:  # pragma: no cover
            case "Bytes":
                multiplier = 1
            case "KiB":
                multiplier = 1024
            case "MiB":
                multiplier = 1024**2
            case "GiB":
                multiplier = 1024**3
            case "TiB":
                multiplier = 1024**4
            case "PiB":
                multiplier = 1024**5
            case _ as unreachable:
                msg = f"Unsupported file size unit: {unreachable!r}"
                raise ParsingError(msg)

        return math.ceil(float(value) * multiplier)

    def infohash(self) -> str:
        selector = '.panel-body > .row > .col-md-offset-6.col-md-1:-soup-contains-own("Info hash:") + .col-md-5'
        return self._body.select_one(selector).get_text()

    def magnet(self) -> str:
        return self._body.select_one('.panel-footer.clearfix > a[href^="magnet:"]').attrs["href"]


class TorrentPageParser:
    """Parser for a full torrent details page, including description and status."""

    __slots__ = ("_base_url", "_body", "_soup")

    def __init__(self, *, html: str, base_url: str) -> None:
        self._soup = SafeSoup(html)
        self._base_url = base_url
        self._body = self._soup.select_one("div:is(.panel.panel-default, .panel.panel-success, .panel.panel-danger)")

    @property
    def panel(self) -> TorrentPanelParser:
        return TorrentPanelParser(body=self._body, base_url=self._base_url)

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

    def pages(self) -> Iterator[PageNumber]:
        pages = self._soup.select("ul.pagination > li:not(.next) > a[href]")
        for page in pages:
            yield PageNumber(int(page.get_text()))

    def results(self) -> Iterator[TorrentID]:
        for id in re.findall(r"<a href=\"(?:/view/(\d+))\" title=\".*\">.*</a>", self._html):
            yield TorrentID(int(id))


def parse_torrent_filename(content_disposition: str) -> str:
    """
    Return the decoded filename from a [`Content-Disposition`][0] header
    as used by [`Nyaa`][1].

    [0]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
    [1]: https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/nyaa/views/torrents.py#L316-L335
    """
    _, filename = content_disposition.split("filename*=UTF-8''")
    return unquote(filename)
