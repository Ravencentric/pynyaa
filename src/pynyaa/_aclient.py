from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

import httpx

from ._bencode import parse_torrent_size
from ._enums import Category, Filter, Order, ParentCategory, SortBy
from ._errors import ReleaseNotFoundError
from ._models import NyaaRelease, TorrentFile
from ._parser import SearchPageParser, TorrentPageParser, parse_torrent_filename
from ._utils import assert_type
from ._version import __version__

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from typing_extensions import Self


async def fetch(client: httpx.AsyncClient, url: str) -> httpx.Response:
    response = await client.get(url)

    # Nyaa *seems* to return 404s for torrents uploaded less than ~3 minutes ago.
    # If you use autobrr, you'll encounter this a lot because the whole point of
    # autobrr is snatching torrents the instant they get announced.
    # We can workaround this by passing junk query paramters to bust the underlying
    # cache and get a fresh result because Nyaa simply ignores all query parameters:
    #
    # <https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/nyaa/views/torrents.py#L18>
    #
    # Unfortunately, this does cost an extra request and a wasted one at that if it's actually a missing page.
    if response.status_code == 404:
        response = await client.get(
            url,
            # The test suite relies on this key being an underscore
            # so don't forget to update those if this ever changes.
            params={"_": time.time_ns()},
        )

    return response


class AsyncNyaa:
    def __init__(self, *, url: str = "https://nyaa.si/", client: httpx.AsyncClient | None = None) -> None:
        """
        Client for interacting with Nyaa.

        Parameters
        ----------
        url : str, optional
            Base URL of Nyaa.
            Used to construct full URLs from relative URLs.
        client : httpx.AsyncClient, optional
            Custom [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient) instance.

        """
        self._url = url
        self._client = (
            httpx.AsyncClient(headers={"User-Agent": f"pynyaa/{__version__} (https://pypi.org/project/pynyaa/)"})
            if client is None
            else client
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        """
        Close the underlying HTTP client session.
        """
        await self._client.aclose()

    async def get(self, page: int | str, /) -> NyaaRelease:
        """
        Fetch metadata for a specific Nyaa release.

        Parameters
        ----------
        page : int or str
            Release ID or full URL (e.g., `123456` or `https://nyaa.si/view/123456`).

        Raises
        ------
        ReleaseNotFoundError
            If the release does not exist (HTTP 404).
        TypeError
            If `page` is not an `int` or `str`.
        ValueError
            If `page` is a string but not a valid release URL.

        Returns
        -------
        NyaaRelease
            Parsed release metadata.

        """
        match page:
            case int():
                id = page
            case str():
                try:
                    id = int(page.rstrip("/").split("/")[-1])
                except ValueError:
                    msg = f"Invalid format for 'page'. Expected a valid URL or numeric ID, but got {page!r}."
                    raise ValueError(msg) from None
            case _:
                msg = f"Parameter 'page' expected 'int' or 'str', but got {type(page).__name__!r}."
                raise TypeError(msg)

        torrent_page_url = urljoin(self._url, f"/view/{id}")
        torrent_file_url = urljoin(self._url, f"/download/{id}.torrent")

        torrent_page, torrent_file = await asyncio.gather(
            fetch(self._client, torrent_page_url),
            fetch(self._client, torrent_file_url),
        )

        if httpx.codes.NOT_FOUND in (torrent_page.status_code, torrent_file.status_code):
            raise ReleaseNotFoundError(torrent_page_url)
        torrent_page.raise_for_status()
        torrent_file.raise_for_status()

        parsed = TorrentPageParser(html=torrent_page.text, url=self._url)

        return NyaaRelease(
            id=id,
            url=torrent_page_url,
            title=parsed.panel.title(),
            category=parsed.panel.category(),
            datetime=parsed.panel.datetime(),
            submitter=parsed.panel.submitter(),
            information=parsed.panel.information(),
            seeders=parsed.panel.seeders(),
            leechers=parsed.panel.leechers(),
            completed=parsed.panel.completed(),
            is_trusted=parsed.is_trusted(),
            is_remake=parsed.is_remake(),
            torrent=TorrentFile(
                name=parse_torrent_filename(torrent_file.headers["Content-Disposition"]),
                data=torrent_file.content,
                size=parse_torrent_size(torrent_file.content),
                infohash=parsed.panel.infohash(),
                url=torrent_file_url,
                magnet=parsed.panel.magnet(),
            ),
            description=parsed.description(),
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
    ) -> AsyncIterator[NyaaRelease]:
        """
        Search for releases on Nyaa.

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
        NyaaRelease
            Parsed release metadata for each search result.

        """
        assert_type(query, str, "query")
        assert_type(category, (ParentCategory, Category), "category")
        assert_type(filter, Filter, "filter")
        assert_type(sort_by, SortBy, "sort_by")
        assert_type(order, Order, "order")

        params: dict[str, Any] = {
            "f": filter,
            "c": category.id,
            "q": query,
            "s": sort_by,
            "o": order,
        }

        # First page
        first = await self._client.get(self._url, params=params)
        first.raise_for_status()
        html = first.text
        parsed = SearchPageParser(html)
        for id in parsed.results():
            yield await self.get(id)

        for page in parsed.pages():  # Second page onwards
            params["p"] = page
            other = await self._client.get(self._url, params=params)
            other.raise_for_status()
            html = other.text
            parsed = SearchPageParser(html)
            for id in parsed.results():
                yield await self.get(id)
