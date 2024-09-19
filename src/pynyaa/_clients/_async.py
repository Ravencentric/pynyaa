from __future__ import annotations

from io import BytesIO
from typing import Any
from urllib.parse import urljoin

from httpx import AsyncClient
from torf import Torrent
from typing_extensions import AsyncGenerator

from pynyaa._enums import Category, Filter, SortBy
from pynyaa._models import NyaaTorrentPage
from pynyaa._parser import parse_nyaa_search_results, parse_nyaa_torrent_page


class AsyncNyaa:
    def __init__(self, base_url: str = "https://nyaa.si/", **kwargs: Any) -> None:
        """
        Async Nyaa client.

        Parameters
        ----------
        base_url : str, optional
            The base URL of Nyaa. Default is `https://nyaa.si/`.
            This is used for constructing the full URL from relative URLs.
        kwargs : Any, optional
            Keyword arguments to pass to the underlying [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient)
            used to make the GET request.
        """
        self._base_url = base_url
        self._kwargs = kwargs

    @property
    def base_url(self) -> str:
        """
        This is the base URL, used for constructing the full URL from relative URLs.
        """
        return self._base_url

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

        async with AsyncClient(**self._kwargs) as client:
            nyaa = await client.get(url)
            nyaa.raise_for_status()

            parsed = parse_nyaa_torrent_page(self._base_url, nyaa.text)

            # Get the torrent file and convert it to a torf.Torrent object
            response = await client.get(parsed["torrent_file"])
            response.raise_for_status()
            torrent = Torrent.read_stream(BytesIO(response.content))

            return NyaaTorrentPage(id=nyaaid, url=url, torrent=torrent, **parsed)  # type: ignore

    async def search(
        self,
        query: str,
        *,
        category: Category = Category.ALL,
        filter: Filter = Filter.NO_FILTER,
        sort_by: SortBy = SortBy.DATETIME,
        reverse: bool = False,
    ) -> AsyncGenerator[NyaaTorrentPage]:
        """
        Search for torrents on Nyaa.

        Parameters
        ----------
        query : str
            The search query.
        category : Category, optional
            The category to narrow down the search results.
        filter : Filter, optional
            Specifies the filter to apply to the search results.
        sort_by : SortBy, optional
            Defines how to sort the results.
        reverse : bool, optional
            Determines the order of the results: ascending if True, descending if False.

        Raises
        ------
        HTTPStatusError
            Nyaa returned a non 2xx response.

        Yields
        -------
        NyaaTorrentPage
            A NyaaTorrentPage object representing the retrieved data.
        """
        async with AsyncClient(**self._kwargs) as client:
            params: dict[str, Any] = dict(
                f=filter,
                c=category.id,
                q=query,
                s=sort_by,
                o="asc" if reverse else "desc",
            )

            nyaa = await client.get(self._base_url, params=params)
            nyaa.raise_for_status()
            results = parse_nyaa_search_results(nyaa.text)

            for link in results:
                yield await self.get(link)
