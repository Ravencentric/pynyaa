from __future__ import annotations

import datetime as dt
import math
import re
from typing import TYPE_CHECKING, Final, NewType
from urllib.parse import urljoin

import bs4

from ._enums import Category
from ._errors import ParsingError
from ._models import Submitter

if TYPE_CHECKING:
    from collections.abc import Iterator

TorrentID = NewType("TorrentID", int)
PageNumber = NewType("PageNumber", int)


class TorrentPanelParser:
    __slots__ = ("_base_url", "_body")

    def __init__(self, *, body: bs4.Tag, base_url: str):
        self._body = body
        self._base_url = base_url

    def select_from_row(self, label: str) -> bs4.Tag:
        if found := self._body.select_one(f'.panel-body > .row > .col-md-1:-soup-contains-own("{label}") + .col-md-5'):
            return found
        msg = f"Could not find required field: {label!r}"
        raise ParsingError(msg)

    def title(self) -> str:
        if title := self._body.select_one(".panel-heading > .panel-title"):
            return title.get_text(strip=True)
        msg = "Missing torrent title."
        raise ParsingError(msg)

    def category(self) -> Category:
        category = self.select_from_row("Category:").get_text().strip()
        return Category(category)

    def datetime(self) -> dt.datetime:
        timestamp = self.select_from_row("Date:").attrs["data-timestamp"]
        return dt.datetime.fromtimestamp(int(timestamp), tz=dt.timezone.utc)

    def submitter(self) -> Submitter | None:
        submitter = self.select_from_row("Submitter:")
        name = submitter.get_text(strip=True)

        if name == "Anonymous":
            return None

        url = urljoin(self._base_url, f"/user/{name}")
        title = submitter.select_one("a").attrs["title"].lower()  # type: ignore[union-attr]
        is_trusted = "trusted" in title
        is_banned = "banned" in title

        return Submitter(name=name, url=url, is_trusted=is_trusted, is_banned=is_banned)

    def seeders(self) -> int:
        return int(self.select_from_row("Seeders:").get_text(strip=True))

    def leechers(self) -> int:
        return int(self.select_from_row("Leechers:").get_text(strip=True))

    def completed(self) -> int:
        return int(self.select_from_row("Completed:").get_text(strip=True))

    def information(self) -> str | None:
        placeholder: Final = "No information."
        information = self.select_from_row("Information:").get_text().strip()
        if information == placeholder:
            return None
        return information

    def size(self) -> int:
        value, unit = self.select_from_row("File size:").get_text(strip=True).split(" ", maxsplit=1)

        match unit:
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
            case _:
                msg = f"Unsupported file size unit: {unit}"
                raise ParsingError(msg)

        return math.ceil(float(value) * multiplier)

    def infohash(self) -> str:
        selector = '.panel-body > .row > .col-md-offset-6.col-md-1:-soup-contains-own("Info hash:") + .col-md-5'
        if found := self._body.select_one(selector):
            return found.get_text(strip=True)
        msg = "Missing torrent info hash."
        raise ParsingError(msg)

    def torrent(self) -> str:
        if found := self._body.select_one('.panel-footer.clearfix > a[href$=".torrent"]'):
            return urljoin(self._base_url, found.attrs["href"])  # type: ignore[no-any-return]
        msg = "Missing torrent download link."
        raise ParsingError(msg)

    def magnet(self) -> str:
        if found := self._body.select_one('.panel-footer.clearfix > a[href^="magnet:"]'):
            return found.attrs["href"]
        msg = "Missing magnet link."
        raise ParsingError(msg)


class TorrentPageParser:
    __slots__ = ("_base_url", "_body", "_soup")

    def __init__(self, *, html: str, base_url: str) -> None:
        self._soup = bs4.BeautifulSoup(html, "html.parser")
        self._base_url = base_url
        if body := self._soup.select_one("div:is(.panel.panel-default, .panel.panel-success, .panel.panel-danger)"):
            self._body = body
        else:
            msg = "Unable to parse the page: malformed structure."
            raise ParsingError(msg)

    @property
    def panel(self) -> TorrentPanelParser:
        return TorrentPanelParser(body=self._body, base_url=self._base_url)

    def is_trusted(self) -> bool:
        return "panel-success" in self._body.attrs["class"]

    def is_remake(self) -> bool:
        return "panel-danger" in self._body.attrs["class"]

    def description(self) -> str | None:
        placeholder: Final = "#### No description."
        if found := self._soup.select_one("#torrent-description"):
            description = found.get_text().strip()
            if description == placeholder:
                return None
            return description
        msg = "Missing torrent description."
        raise ParsingError(msg)


class SearchPageParser:
    __slots__ = ("_html", "_soup")

    def __init__(self, html: str) -> None:
        self._html = html
        self._soup = bs4.BeautifulSoup(html, "html.parser")

    def pages(self) -> Iterator[PageNumber]:
        pages = self._soup.select("ul.pagination > li:not(.next) > a[href]")
        for page in pages:
            yield PageNumber(int(page.get_text(strip=True)))

    def results(self) -> Iterator[TorrentID]:
        for id in re.findall(r"<a href=\"(?:/view/(\d+))\" title=\".*\">.*</a>", self._html):
            yield TorrentID(int(id))
