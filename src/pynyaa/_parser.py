from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from xmltodict import parse as xmltodict_parse


def parse_nyaa_torrent_page(base_url: str, html: str) -> dict[str, Any]:
    """
    Parse the HTML page to extract relevant information

    Parameters
    ----------
    base_url : str
        Base URL used to construct the full URL from relative URLs.
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
    category = row_one[0].get_text().strip()
    date = row_one[1]["data-timestamp"]

    # ROW TWO
    row_two = rows[1].find_all("div", class_="col-md-5")
    submitter = row_two[0].get_text().strip()
    if submitter.lower() != "anonymous":
        submitter_url = urljoin(base_url, row_two[0].find("a").get("href", f"/user/{submitter}"))
        submitter_status = row_two[0].find("a").get("title", None)

        if submitter_status is not None:
            if submitter_status.lower() == "trusted":
                submitter_trusted = True
                submitter_banned = False
            elif submitter_status.lower() == "banned user":
                submitter_trusted = False
                submitter_banned = True
            elif submitter_status.lower() == "banned trusted":
                submitter_trusted = True
                submitter_banned = True
            else:
                submitter_trusted = False
                submitter_banned = False
    else:
        submitter_url = base_url
        submitter_trusted = False
        submitter_banned = False

    seeders = row_two[1].get_text().strip()

    # ROW THREE
    row_three = rows[2].find_all("div", class_="col-md-5")
    information = row_three[0].get_text().strip()
    leechers = row_three[1].get_text().strip()

    # ROW FOUR
    row_four = rows[3].find_all("div", class_="col-md-5")
    completed = row_four[1].get_text().strip()

    # ROW FOOTER
    footer = body.find("div", class_="panel-footer clearfix").find_all("a")  # type: ignore
    torrent_file = urljoin(base_url, footer[0]["href"])
    magnet = footer[1]["href"]

    # DESCRIPTION
    description = soup.find(id="torrent-description").get_text().strip()  # type: ignore

    return dict(
        title=title,
        category=category,
        date=date,
        submitter=dict(
            name=submitter,
            url=submitter_url,
            is_trusted=submitter_trusted,
            is_banned=submitter_banned,
        ),
        information=information,
        seeders=seeders,
        leechers=leechers,
        completed=completed,
        is_trusted=is_trusted,
        is_remake=is_remake,
        description=description,
        torrent_file=torrent_file,
        magnet=magnet,
    )


def parse_nyaa_rss_page(xml: str, limit: int) -> tuple[str, ...]:
    """
    Parse the torrent links out of the RSS page

    Parameters
    ----------
    xml : str
        Nyaa's RSS XML data as a string
    limit : str
        Maximum number of links to parse out of the RSS page

    Returns
    -------
    tuple[str, ...]
        A tuple of torrent links
    """
    try:
        items = xmltodict_parse(xml, encoding="utf-8")["rss"]["channel"]["item"]
    except KeyError:
        return tuple()

    if isinstance(items, dict):  # RSS returns single results as a dict instead of a list
        items = [items]

    if limit > len(items):
        parsed = [item["guid"]["#text"] for item in items]
    else:
        parsed = [item["guid"]["#text"] for item in items[:limit]]

    return tuple(parsed)
