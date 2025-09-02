from __future__ import annotations

import datetime as dt
import math
import re
from typing import Final
from urllib.parse import urljoin

import bs4

from ._enums import Category
from ._errors import ParsingError
from ._models import NyaaTorrentPage, Submitter

NO_INFORMATION: Final = "No information."
NO_DESCRIPTION: Final = "#### No description."


def urlfor(endpoint: str) -> str:
    return urljoin("https://nyaa.si/", endpoint)

class PanelExtractor:
    __slots__ = ("_body",)

    def __init__(self, body: bs4.Tag):
        self._body = body

    def select_from_row(self, label: str) -> bs4.Tag:
        if found := self._body.select_one(f'.panel-body > .row > .col-md-1:-soup-contains-own("{label}") + .col-md-5'):
            return found
        raise ParsingError(f"Could not find required field: {label!r}")

    def title(self) -> str:
        if title := self._body.select_one(".panel-heading > .panel-title"):
            return title.get_text(strip=True)
        raise ParsingError("Missing torrent title.")

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

        url = urlfor(f"/user/{name}")
        title = submitter.select_one("a").attrs["title"].lower()  # type: ignore
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

    def filesize(self) -> int:
        value, unit = self.select_from_row("File size:").get_text(strip=True).split(" ", maxsplit=1)

        match unit:
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
                raise ParsingError(f"Unsupported file size unit: {unit}")

        return math.ceil(float(value) * multiplier)

    def infohash(self) -> str:
        selector = '.panel-body > .row > .col-md-offset-6.col-md-1:-soup-contains-own("Info hash:") + .col-md-5'
        if found := self._body.select_one(selector):
            return found.get_text(strip=True)
        raise ParsingError("Missing torrent info hash.")

    def torrent(self) -> str:
        if found := self._body.select_one('.panel-footer.clearfix > a[href$=".torrent"]'):
            return urlfor(found.attrs["href"])
        raise ParsingError("Missing torrent download link.")

    def magnet(self) -> str:
        if found := self._body.select_one('.panel-footer.clearfix > a[href^="magnet:"]'):
            return found.attrs["href"]
        raise ParsingError("Missing magnet link.")


class PageExtractor:
    __slots__ = ("_soup", "_body")

    def __init__(self, html: str) -> None:
        self._soup = bs4.BeautifulSoup(html, "lxml")
        if body := self._soup.select_one("div:is(.panel.panel-default, .panel.panel-success, .panel.panel-danger)"):
            self._body = body
        else:
            raise ParsingError("Unable to parse the page: malformed structure.")

    def panel(self) -> PanelExtractor:
        return PanelExtractor(self._body)

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
        raise ParsingError("Missing torrent description.")

def parse_nyaa_torrent_page(id: int, html: str) -> NyaaTorrentPage:
    """
    Parse the HTML page to extract relevant information

    Parameters
    ----------
    id : int
        ID of the torrent.
    html : str
        HTML content of the Nyaa page.

    Returns
    -------
    dict[str, Any]
        A dictionary with the relevant information.
    """

    page = PageExtractor(html)
    panel = page.panel()

    return NyaaTorrentPage(
        id=id,
        url=urlfor(f"/view/{id}"),
        title=panel.title(),
        category=panel.category(),
        datetime=panel.datetime(),
        submitter=panel.submitter(),
        information=panel.information(),
        seeders=panel.seeders(),
        leechers=panel.leechers(),
        completed=panel.completed(),
        is_trusted=page.is_trusted(),
        is_remake=page.is_remake(),
        description=page.description(),
        torrent=panel.torrent(),
        magnet=panel.magnet(),
    )


def parse_nyaa_search_results(html: str, base_url: str = "https://nyaa.si") -> tuple[str, ...]:
    """
    Parses the HTML of a Nyaa search results page to extract torrent links.

    Parameters
    ----------
    html : str
        The HTML content of the Nyaa search results page.
    base_url : str, optional
        The base URL to use for constructing full links from relative links.

    Yields
    ------
    str
        The full URL of torrent page, in the order they were present.
    """
    parsed = re.findall(r"<a href=\"(/view/\d+)\" title=\".*\">.*</a>", html)
    return tuple(urljoin(base_url, relative_link) for relative_link in parsed)
