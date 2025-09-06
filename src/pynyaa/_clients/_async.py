from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

import bs4
import httpx

from pynyaa._enums import Category, Filter, ParentCategory, SortBy
from pynyaa._errors import TorrentNotFoundError
from pynyaa._models import NyaaTorrentPage
from pynyaa._parser import PageParser, parse_nyaa_search_results
from pynyaa._utils import assert_type
from pynyaa._version import __version__

if TYPE_CHECKING:
    from typing_extensions import AsyncIterator, Self


class AsyncNyaa:
    def __init__(self, base_url: str = "https://nyaa.si/", client: httpx.AsyncClient | None = None) -> None:
        """
        A client for interacting with Nyaa.

        Parameters
        ----------
        base_url : str, optional
            The base URL of Nyaa.
            This is used for constructing the full URL from relative URLs.
        client : AsyncClient, optional
            An [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient) instance used to make requests to Nyaa.
        """
        self._base_url = base_url
        self._client = httpx.AsyncClient(headers={"user-agent": f"pynyaa/{__version__}"}) if client is None else client

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

    async def get(self, page: int | str, /) -> NyaaTorrentPage:
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
        TorrentNotFoundError
            Nyaa returned a non 2xx response.
        TypeError
            If the 'page' parameter is not an int or str.

        Returns
        -------
        NyaaTorrentPage
            A NyaaTorrentPage object representing the retrieved data.
        """

        match page:
            case int():
                id = page
            case str():
                try:
                    id = int(page.rstrip("/").split("/")[-1])
                except ValueError:
                    raise ValueError(
                        f"Invalid format for 'page'. Expected a valid URL or numeric ID, but got {page!r}."
                    )
            case _:
                raise TypeError(f"Parameter 'page' expected 'int' or 'str', but got {type(page).__name__!r}.")

        url = urljoin(self._base_url, f"/view/{id}")
        nyaa = await self._client.get(url)

        if nyaa.status_code == httpx.codes.NOT_FOUND:
            raise TorrentNotFoundError(url)
        else:
            nyaa.raise_for_status()

        parsed = PageParser(html=nyaa.text, base_url=self.base_url)
        panel = parsed.panel()

        return NyaaTorrentPage(
            id=id,
            url=url,
            title=panel.title(),
            category=panel.category(),
            datetime=panel.datetime(),
            submitter=panel.submitter(),
            information=panel.information(),
            seeders=panel.seeders(),
            leechers=panel.leechers(),
            completed=panel.completed(),
            size=panel.filesize(),
            infohash=panel.infohash(),
            is_trusted=parsed.is_trusted(),
            is_remake=parsed.is_remake(),
            description=parsed.description(),
            torrent=panel.torrent(),
            magnet=panel.magnet(),
        )

    async def search(
        self,
        query: str,
        *,
        category: ParentCategory | Category = ParentCategory.ALL,
        filter: Filter = Filter.NO_FILTER,
        sort_by: SortBy = SortBy.DATETIME,
        reverse: bool = False,
    ) -> AsyncIterator[NyaaTorrentPage]:
        """
        Search for torrents on Nyaa.

        Parameters
        ----------
        query : str
            The search query.
        category : ParentCategory | Category, optional
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
        assert_type(query, str, "query")
        assert_type(category, (ParentCategory, Category), "category")
        assert_type(filter, Filter, "filter")
        assert_type(sort_by, SortBy, "sort_by")
        assert_type(reverse, bool, "reverse")

        params: dict[str, Any] = dict(
            f=filter,
            c=category.id,
            q=query,
            s=sort_by,
            o="asc" if reverse else "desc",  # desc is the default on nyaa
        )

        first = await self._client.get(self._base_url, params=params)
        first.raise_for_status()
        html = first.text
        for link in parse_nyaa_search_results(html):
            yield await self.get(link)

        # This selector does NOT return page 1, starts with 2 and that's exactly what we want.
        pages = bs4.BeautifulSoup(html, "lxml").select("ul.pagination > li:not(.next) > a[href]")
        for page in pages:
            params["p"] = page.get_text()  # 2, 3, ...
            other = await self._client.get(self._base_url, params=params)
            other.raise_for_status()
            html = other.text
            for link in parse_nyaa_search_results(html):
                yield await self.get(link)
