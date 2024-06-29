from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from hishel import AsyncCacheClient, AsyncFileStorage
from pydantic import validate_call
from pydantic_core import Url
from torf import Torrent
from xmltodict import parse as xmltodict_parse

from .._enums import NyaaCategory, NyaaFilter
from .._models import NyaaTorrentPage
from .._types import SearchLimit
from .._utils import _get_user_cache_path


class AsyncNyaa:
    @validate_call
    def __init__(self, base_url: str = "https://nyaa.si/", cache: bool = True, **kwargs: Any) -> None:
        """
        Async Nyaa client.

        Parameters
        ----------
        base_url : str, optional
            The base URL of Nyaa. Default is `https://nyaa.si/`.
            This is used for constructing the full URL from relative URLs.
        cache : bool, optional
            Whether to enable caching. Default is `True`.
            This will cache the page upon it's first request and then use the cached result
            for any subsequent requests for the same page.
            This helps in avoiding [HTTP 429 Error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) but
            do note some fields like seeders, leechers, and completed are constantly changing and thus caching would
            mean you won't get the latest data on said fields.
        kwargs : Any, optional
            Keyword arguments to pass to the underlying [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient)
            used to make the GET request.
        """
        self._base_url = base_url
        self._cache = cache
        self._kwargs = kwargs
        self._extensions = {"force_cache": self._cache, "cache_disabled": not self._cache}
        self._storage = AsyncFileStorage(base_path=_get_user_cache_path())

    @property
    def base_url(self) -> str:
        """
        This is the base URL, used for constructing the full URL from relative URLs.
        """
        return self._base_url

    @property
    def cache_path(self) -> Path:
        """
        Path where cache files are stored.
        """
        return _get_user_cache_path()

    async def _parse_nyaa(self, html: str) -> dict[str, Any]:
        """
        Parse the HTML page to extract relevant information

        Parameters
        ----------
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
            submitter_url = urljoin(self._base_url, row_two[0].find("a").get("href", f"/user/{submitter}"))
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
            submitter_url = self._base_url
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
        torrent_file = urljoin(self._base_url, footer[0]["href"])
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

    @validate_call
    async def get(self, page: int | str) -> NyaaTorrentPage:
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

        Returns
        -------
        NyaaTorrentPage
            A NyaaTorrentPage object representing the retrieved data.
        """

        if isinstance(page, int):
            url = urljoin(self._base_url, f"/view/{page}")
            id = page
        else:
            url = page
            id = page.split("/")[-1]  # type: ignore
            host = Url(page).host
            self._base_url = f"https://{host}/" if host is not None else "https://nyaa.si/"

        async with AsyncCacheClient(storage=self._storage, **self._kwargs) as client:
            nyaa = await client.get(url, extensions=self._extensions)
            nyaa.raise_for_status()

            info = await self._parse_nyaa(nyaa.text)

            # Get the torrent file and convert it to a torf.Torrent object
            response = await client.get(info["torrent_file"], extensions=self._extensions)
            response.raise_for_status()
            torrent = Torrent.read_stream(BytesIO(response.content))

            return NyaaTorrentPage(
                id=id,  # type: ignore
                url=url,  # type: ignore
                torrent=torrent,
                **info,
            )

    @validate_call
    async def search(
        self,
        query: str,
        *,
        category: NyaaCategory | None = None,
        filter: NyaaFilter | None = None,
        limit: SearchLimit = 3,
    ) -> tuple[NyaaTorrentPage, ...]:
        """
        Search for torrents on Nyaa.

        Parameters
        ----------
        query : str
            The search query string.
        category : NyaaCategory, optional
            The category to filter the search. If None, searches all categories.
        filter : NyaaFilter, optional
            The filter to apply to the search results. If None, no filter is applied.
        limit : SearchLimit, optional
            Maximum number of search results to retrieve. Defaults to 3. Maximum is 75.
            Be cautious with this; higher limits increase the number of requests,
            which may trigger rate limiting responses (HTTP 429) or get your IP banned entirely.

        Raises
        ------
        ValidationError
            Invalid input
        HTTPStatusError
            Nyaa returned a non 2xx response.

        Returns
        -------
        tuple[NyaaTorrentPage, ...]
            A tuple of NyaaTorrentPage objects representing the retrieved data.
        """
        async with AsyncCacheClient(storage=self._storage, **self._kwargs) as client:
            params = dict(
                page="rss",
                f=filter if filter is not None else 0,
                c=category.id if category is not None else "0_0",
                q=query,
            )

            nyaa = await client.get(self._base_url, params=params, extensions=self._extensions)  # type: ignore
            nyaa.raise_for_status()

            try:
                items = xmltodict_parse(nyaa.text, encoding="utf-8")["rss"]["channel"]["item"]
            except KeyError:
                return tuple()

            if isinstance(items, dict):  # RSS returns single results as a dict instead of a list
                items = [items]

            if limit > len(items):
                parsed = [await self.get(item["guid"]["#text"]) for item in items]
            else:
                parsed = [await self.get(item["guid"]["#text"]) for item in items[:limit]]

            return tuple(parsed)
