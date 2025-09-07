"""Turn nyaa.si torrent pages into neat Python objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from pynyaa._clients._async import AsyncNyaa
from pynyaa._clients._sync import Nyaa
from pynyaa._enums import Category, Filter, Order, ParentCategory, SortBy
from pynyaa._errors import ParsingError, PyNyaaError, TorrentNotFoundError
from pynyaa._models import NyaaTorrentPage, Submitter
from pynyaa._version import __version__

if TYPE_CHECKING:
    from collections.abc import Iterator


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
    category: ParentCategory | Category = ParentCategory.ALL,
    filter: Filter = Filter.NO_FILTER,
    sort_by: SortBy = SortBy.DATETIME,
    order: Order = Order.DESCENDING,
) -> Iterator[NyaaTorrentPage]:  # pragma: no cover
    """
    Shortcut for `pynyaa.Nyaa.search`.
    For more advanced or configurable usage, use the `pynyaa.Nyaa` client directly.
    """
    with Nyaa() as nyaa:
        yield from nyaa.search(query, category=category, filter=filter, sort_by=sort_by, order=order)


__all__: Final = (
    "AsyncNyaa",
    "Category",
    "Filter",
    "Nyaa",
    "NyaaTorrentPage",
    "Order",
    "ParentCategory",
    "ParsingError",
    "PyNyaaError",
    "SortBy",
    "Submitter",
    "TorrentNotFoundError",
    "__version__",
    "get",
    "search",
)
