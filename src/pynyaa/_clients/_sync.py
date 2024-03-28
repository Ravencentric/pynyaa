from __future__ import annotations

from io import BytesIO
from typing import Any

from bs4 import BeautifulSoup
from hishel import CacheClient, FileStorage
from pydantic import validate_call
from pydantic_core import Url
from torf import Torrent

from .._exceptions import HTMLParsingError
from .._models import NyaaTorrentPage
from .._types import HTTPXClientKwargs
from .._utils import _get_user_cache_path


class Nyaa:
    def __init__(self, base_url: str = "https://nyaa.si", cache: bool = True, **kwargs: HTTPXClientKwargs) -> None:
        """
        Nyaa client.

        Parameters
        ----------
        base_url : str, optional
            The base URL of Nyaa. Default is `https://nyaa.si`.
            This is only used when a Nyaa ID is passed.
            If a full URL is passed then this gets ignored and the base_url is parsed from the given URL instead.
        cache : bool, optional
            Whether to enable caching. Default is `True`.
            This will cache the page upon it's first request and then use the cached result
            for any subsequent requests for the same page.
            This helps in avoiding [HTTP 429 Error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) but
            do note some fields like seeders, leechers, and completed are constantly changing and thus caching would
            mean you won't get the latest data on said fields.
        kwargs : HTTPXClientKwargs, optional
            Keyword arguments to pass to the underlying [httpx.Client()](https://www.python-httpx.org/api/#client)
            used to make the GET request.
        """
        self.base_url = base_url.strip("/")
        self.cache = cache
        self.kwargs = kwargs

    def _parse_nyaa(self, html: str) -> dict[str, Any]:
        """
        Parse the HTML page to extract relevant information

        Parameters
        ----------
        html : str
            HTML content of the Nyaa page.

        Raises
        ------
        HTMLParsingError
            Raised for any error encountered while parsing Nyaa's HTML content

        Returns
        -------
        dict[str, Any]
            A dictionary with the relevant information.
        """

        try:
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

            title = soup.title.string.strip(":: Nyaa").strip()  # type: ignore

            rows = body.find("div", class_="panel-body").find_all("div", class_="row")  # type: ignore

            # ROW ONE
            row_one = rows[0].find_all("div", class_="col-md-5")
            category = row_one[0].get_text().strip()
            date = row_one[1]["data-timestamp"]

            # ROW TWO
            row_two = rows[1].find_all("div", class_="col-md-5")
            submitter = row_two[0].get_text().strip()
            if submitter.lower() != "anonymous":
                submitter_url = f"{self.base_url}{row_two[0].find('a').get('href', f'/user/{submitter}')}"
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
                submitter_url = self.base_url
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
            torrent_file = f"{self.base_url}{footer[0]['href']}"
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
        except Exception as error:
            raise HTMLParsingError("Encountered an error while parsing Nyaa's HTML content!") from error

    @validate_call
    def get(self, page: int | str) -> NyaaTorrentPage:
        """
        Retrieve information from a Nyaa torrent page.

        Parameters
        ----------
        page : int or str
            The torrent page.
            This can either be a URL like `https://nyaa.si/view/123456`
            or just the ID like `123456`

        Raises
        ------
        ValidationError
            Invalid input
        HTTPStatusError
            Nyaa returned a non 2xx response.
        HTMLParsingError
            Raised for any error encountered while parsing Nyaa's HTML content

        Returns
        -------
        NyaaTorrentPage
            A NyaaTorrentPage object representing the retrieved data.
        """

        if isinstance(page, int):
            url = f"{self.base_url}/view/{page}"
            id = page
        else:
            url = page
            id = page.split("/")[-1]  # type: ignore
            host = Url(page).host
            self.base_url = f"https://{host}" if host is not None else "https://nyaa.si"

        with CacheClient(storage=FileStorage(base_path=_get_user_cache_path()), **self.kwargs) as client:
            extensions = {"force_cache": self.cache, "cache_disabled": not self.cache}
            nyaa = client.get(url, extensions=extensions).raise_for_status()

            info = self._parse_nyaa(nyaa.text)

            # Get the torrent file and convert it to a torf.Torrent object
            torrent = Torrent.read_stream(
                BytesIO(client.get(info["torrent_file"], extensions=extensions).raise_for_status().content)
            )

            return NyaaTorrentPage(
                id=id,  # type: ignore
                url=url,  # type: ignore
                torrent=torrent,
                **info,
            )
