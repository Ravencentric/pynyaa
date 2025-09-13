"""Turn nyaa.si releases into neat Python objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ._aclient import AsyncNyaa
from ._client import Nyaa
from ._enums import Category, Filter, Order, ParentCategory, SortBy
from ._errors import ParsingError, PyNyaaError, ReleaseNotFoundError
from ._models import NyaaRelease, Submitter, TorrentFile
from ._version import __version__

if TYPE_CHECKING:
    from collections.abc import Iterator


def get(page: int | str) -> NyaaRelease:  # pragma: no cover
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
) -> Iterator[NyaaRelease]:  # pragma: no cover
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
    "NyaaRelease",
    "Order",
    "ParentCategory",
    "ParsingError",
    "PyNyaaError",
    "ReleaseNotFoundError",
    "SortBy",
    "Submitter",
    "TorrentFile",
    "__version__",
    "get",
    "search",
)
