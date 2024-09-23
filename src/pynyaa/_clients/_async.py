from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

from httpx import AsyncClient
from torf import Torrent

from pynyaa._enums import Category, Filter, SortBy
from pynyaa._models import NyaaTorrentPage
from pynyaa._parser import parse_nyaa_search_results, parse_nyaa_torrent_page
from pynyaa._version import __version__

if TYPE_CHECKING:
    from typing_extensions import AsyncGenerator, Self


class AsyncNyaa:
    def __init__(self, base_url: str = "https://nyaa.si/", client: AsyncClient | None = None) -> None:
        """
        Async Nyaa client.

        Parameters
        ----------
        base_url : str, optional
            The base URL of Nyaa.
            This is used for constructing the full URL from relative URLs.
        client : Client, optional
            An [`httpx.Client`](https://www.python-httpx.org/api/#client) instance used to make requests to Nyaa.
        """
        self._base_url = base_url
        self._client = AsyncClient(headers={"user-agent": f"pynyaa/{__version__}"}) if client is None else client

    @property
    def base_url(self) -> str:
        """
        This is the base URL, used for constructing the full URL from relative URLs.
        """
        return self._base_url

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the connection"""
        await self._client.aclose()

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

        nyaa_id = page if isinstance(page, int) else page.split("/")[-1]
        nyaa_url = urljoin(self._base_url, f"/view/{nyaa_id}")

        nyaa = await self._client.get(nyaa_url)
        nyaa.raise_for_status()

        parsed = parse_nyaa_torrent_page(self._base_url, nyaa.text)

        # Get the torrent file and convert it to a torf.Torrent object
        response = await self._client.get(parsed["torrent_file"])
        response.raise_for_status()
        torrent = Torrent.read_stream(BytesIO(response.content))

        return NyaaTorrentPage(id=nyaa_id, url=nyaa_url, torrent=torrent, **parsed)  # type: ignore

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
            Determines the order of the results: ascending if `True`, descending if `False`.

        Raises
        ------
        HTTPStatusError
            Nyaa returned a non 2xx response.

        Yields
        -------
        NyaaTorrentPage
            A NyaaTorrentPage object representing the retrieved data.
        """
        params: dict[str, Any] = dict(
            f=filter,
            c=category.id,
            q=query,
            s=sort_by,
            o="asc" if reverse else "desc",  # desc is the default on nyaa
        )

        nyaa = await self._client.get(self._base_url, params=params)
        nyaa.raise_for_status()
        results = parse_nyaa_search_results(nyaa.text)

        for link in results:
            yield await self.get(link)
