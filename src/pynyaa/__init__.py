from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import HTTPStatusError

from pynyaa._clients._async import AsyncNyaa
from pynyaa._clients._sync import Nyaa
from pynyaa._enums import Category, Filter, SortBy
from pynyaa._models import NyaaTorrentPage, Submitter
from pynyaa._version import __version__, __version_tuple__

if TYPE_CHECKING:
    from typing_extensions import Generator


def get(page: int | str) -> NyaaTorrentPage:  # pragma: no cover
    """
    Shortcut for `pynyaa.Nyaa.get`.
    For more advanced or configurable usage, use the `pynyaa.Nyaa` client directly.
    """
    with Nyaa() as nyaa:
        return nyaa.get(page)


def search(
    query: str,
    *,
    category: Category = Category.ALL,
    filter: Filter = Filter.NO_FILTER,
    sort_by: SortBy = SortBy.DATETIME,
    reverse: bool = False,
) -> Generator[NyaaTorrentPage]:  # pragma: no cover
    """
    Shortcut for `pynyaa.Nyaa.search`.
    For more advanced or configurable usage, use the `pynyaa.Nyaa` client directly.
    """
    with Nyaa() as nyaa:
        yield from nyaa.search(query, category=category, filter=filter, sort_by=sort_by, reverse=reverse)


__all__ = (
    # Clients
    "AsyncNyaa",
    "Nyaa",
    # Top level API,
    "get",
    "search",
    # Enums
    "Category",
    "Filter",
    "SortBy",
    # Models
    "NyaaTorrentPage",
    "Submitter",
    # Exceptions
    "HTTPStatusError",
    # Version
    "__version__",
    "__version_tuple__",
)
