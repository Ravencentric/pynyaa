from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

import bs4
import httpx

from pynyaa._enums import Category, Filter, Order, ParentCategory, SortBy
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
            Base URL of Nyaa.
            Used to construct full URLs from relative paths.
        client : httpx.AsyncClient, optional
            Custom [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient) instance.
        """
        self._base_url = base_url
        self._client = (
            httpx.AsyncClient(headers={"User-Agent": f"pynyaa/{__version__} (https://pypi.org/project/pynyaa/)"})
            if client is None
            else client
        )

    @property
    def base_url(self) -> str:
        """
        Base URL of Nyaa.
        Used to construct full URLs from relative paths.
        """
        return self._base_url

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        """
        Close the underlying HTTP client session.
        """
        await self._client.aclose()

    async def get(self, page: int | str, /) -> NyaaTorrentPage:
        """
        Fetch metadata for a specific torrent page.

        Parameters
        ----------
        page : int or str
            Torrent ID or full URL (e.g., `123456` or `https://nyaa.si/view/123456`).

        Raises
        ------
        TorrentNotFoundError
            If the torrent does not exist (HTTP 404).
        TypeError
            If `page` is not an `int` or `str`.
        ValueError
            If `page` is a string but not a valid torrent URL.

        Returns
        -------
        NyaaTorrentPage
            Parsed torrent metadata as a `NyaaTorrentPage` object.
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
        nyaa.raise_for_status()

        parsed = PageParser(html=nyaa.text, base_url=self.base_url)

        return NyaaTorrentPage(
            id=id,
            url=url,
            title=parsed.panel.title(),
            category=parsed.panel.category(),
            datetime=parsed.panel.datetime(),
            submitter=parsed.panel.submitter(),
            information=parsed.panel.information(),
            seeders=parsed.panel.seeders(),
            leechers=parsed.panel.leechers(),
            completed=parsed.panel.completed(),
            size=parsed.panel.size(),
            infohash=parsed.panel.infohash(),
            is_trusted=parsed.is_trusted(),
            is_remake=parsed.is_remake(),
            description=parsed.description(),
            torrent=parsed.panel.torrent(),
            magnet=parsed.panel.magnet(),
        )

    async def search(
        self,
        query: str,
        /,
        *,
        category: ParentCategory | Category = ParentCategory.ALL,
        filter: Filter = Filter.NO_FILTER,
        sort_by: SortBy = SortBy.DATETIME,
        order: Order = Order.DESCENDING,
    ) -> AsyncIterator[NyaaTorrentPage]:
        """
        Search for torrents on Nyaa.

        Parameters
        ----------
        query : str
            Search query string.
        category : ParentCategory | Category, optional
            Category or subcategory used to filter results.
        filter : Filter, optional
            Filter applied to the search results.
        sort_by : SortBy, optional
            Field used to sort the results.
        order : Order, optional
            Order of the results.

        Yields
        ------
        NyaaTorrentPage
            Parsed torrent metadata for each result.
        """
        assert_type(query, str, "query")
        assert_type(category, (ParentCategory, Category), "category")
        assert_type(filter, Filter, "filter")
        assert_type(sort_by, SortBy, "sort_by")
        assert_type(order, Order, "order")

        params: dict[str, Any] = dict(
            f=filter,
            c=category.id,
            q=query,
            s=sort_by,
            o=order,
        )

        # Fetch the first page of results
        first = await self._client.get(self._base_url, params=params)
        first.raise_for_status()
        html = first.text
        for link in parse_nyaa_search_results(html):
            yield await self.get(link)

        # Pagination links start at page 2 (page 1 is already handled)
        pages = bs4.BeautifulSoup(html, "lxml").select("ul.pagination > li:not(.next) > a[href]")
        for page in pages:
            params["p"] = page.get_text()
            other = await self._client.get(self._base_url, params=params)
            other.raise_for_status()
            html = other.text
            for link in parse_nyaa_search_results(html):
                yield await self.get(link)
