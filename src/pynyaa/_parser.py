from __future__ import annotations

import datetime as dt
import re
from typing import Final
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ._enums import Category
from ._models import NyaaTorrentPage, Submitter

NO_INFORMATION: Final = "No information."
NO_DESCRIPTION: Final = "#### No description."


def urlfor(endpoint: str) -> str:
    return urljoin("https://nyaa.si/", endpoint)


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

    soup = BeautifulSoup(html, "lxml")

    if success := soup.find("div", class_="panel panel-success"):
        # Trusted uploads use `panel-success` for their green color
        body = success
        is_trusted = True
        is_remake = False
    elif remake := soup.find("div", class_="panel panel-danger"):
        # Remake uploads use `panel-danger` for their red color
        body = remake
        is_trusted = False
        is_remake = True
    else:
        # Default uploads use `panel-default`
        body = soup.find("div", class_="panel panel-default")  # type: ignore
        is_trusted = False
        is_remake = False

    title = soup.title.string.replace(":: Nyaa", "").strip()  # type: ignore

    rows = body.find("div", class_="panel-body").find_all("div", class_="row")  # type: ignore

    # ROW ONE
    row_one = rows[0].find_all("div", class_="col-md-5")
    category = Category(row_one[0].get_text().strip())
    datetime = dt.datetime.fromtimestamp(int(row_one[1]["data-timestamp"]), tz=dt.timezone.utc)

    # ROW TWO
    row_two = rows[1].find_all("div", class_="col-md-5")
    submitter_name = row_two[0].get_text().strip()
    submitter: Submitter | None = None

    if submitter_name != "Anonymous":
        submitter_url = urlfor(f"/user/{submitter_name}")
        submitter_status: str = row_two[0].find("a").get("title", "default")

        match submitter_status.lower():
            case "trusted":
                submitter = Submitter(name=submitter_name, url=submitter_url, is_trusted=True, is_banned=False)
            case "banned user":
                submitter = Submitter(name=submitter_name, url=submitter_url, is_trusted=False, is_banned=True)
            case "banned trusted":
                submitter = Submitter(name=submitter_name, url=submitter_url, is_trusted=True, is_banned=True)
            case _:
                submitter = Submitter(name=submitter_name, url=submitter_url, is_trusted=False, is_banned=False)
    else:
        submitter = None

    seeders = int(row_two[1].get_text().strip())

    # ROW THREE
    row_three = rows[2].find_all("div", class_="col-md-5")
    information: str | None = None
    if _information := row_three[0].get_text().strip():
        if _information != NO_INFORMATION:
            information = _information
    leechers = int(row_three[1].get_text().strip())

    # ROW FOUR
    row_four = rows[3].find_all("div", class_="col-md-5")
    completed = int(row_four[1].get_text().strip())

    # ROW FOOTER
    footer = body.find("div", class_="panel-footer clearfix").find_all("a")  # type: ignore
    torrent = urlfor(footer[0]["href"])
    magnet = footer[1]["href"]

    # DESCRIPTION
    description: str | None = None
    if _description := soup.find(id="torrent-description").get_text().strip():  # type: ignore
        if _description != NO_DESCRIPTION:
            description = _description

    return NyaaTorrentPage(
        id=id,
        url=urlfor(f"/view/{id}"),
        title=title,
        category=category,
        datetime=datetime,
        submitter=submitter,
        information=information,
        seeders=seeders,
        leechers=leechers,
        completed=completed,
        is_trusted=is_trusted,
        is_remake=is_remake,
        description=description if description else None,
        torrent=torrent,
        magnet=magnet,
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
