from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from hishel import CacheClient, FileStorage
from pydantic import validate_call
from torf import Torrent

from .._enums import NyaaCategory, NyaaFilter
from .._models import NyaaTorrentPage
from .._parser import parse_nyaa_rss_page, parse_nyaa_torrent_page
from .._types import SearchLimit
from .._utils import get_user_cache_path


class Nyaa:
    @validate_call
    def __init__(self, base_url: str = "https://nyaa.si/", cache: bool = True, **kwargs: Any) -> None:
        """
        Nyaa client.

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
            Keyword arguments to pass to the underlying [`httpx.Client`](https://www.python-httpx.org/api/#client)
            used to make the GET request.
        """
        self._base_url = base_url
        self._cache = cache
        self._kwargs = kwargs
        self._extensions = {"force_cache": self._cache, "cache_disabled": not self._cache}
        self._storage = FileStorage(base_path=get_user_cache_path())

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
        return get_user_cache_path()

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

        Returns
        -------
        NyaaTorrentPage
            A NyaaTorrentPage object representing the retrieved data.
        """

        if isinstance(page, int):
            url = urljoin(self._base_url, f"/view/{page}")
            nyaaid = page
        else:
            url = page
            nyaaid = page.split("/")[-1]  # type: ignore

        with CacheClient(storage=self._storage, **self._kwargs) as client:
            nyaa = client.get(url, extensions=self._extensions).raise_for_status()
            parsed = parse_nyaa_torrent_page(self._base_url, nyaa.text)

            # Get the torrent file and convert it to a torf.Torrent object
            torrent_file = client.get(parsed["torrent_file"], extensions=self._extensions).raise_for_status().content
            torrent = Torrent.read_stream(BytesIO(torrent_file))

            return NyaaTorrentPage(id=nyaaid, url=url, torrent=torrent, **parsed)  # type: ignore

    @validate_call
    def search(
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
        with CacheClient(storage=self._storage, **self._kwargs) as client:
            params = dict(
                page="rss",
                f=filter if filter is not None else 0,
                c=category.id if category is not None else "0_0",
                q=query,
            )

            nyaa = client.get(self._base_url, params=params, extensions=self._extensions).raise_for_status()  # type: ignore
            results = parse_nyaa_rss_page(nyaa.text, limit)

            parsed = [self.get(link) for link in results]

            return tuple(parsed)
