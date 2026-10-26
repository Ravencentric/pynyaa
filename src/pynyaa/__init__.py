# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

"""Turn nyaa.si releases into neat Python objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ._aclient import AsyncNyaa
from ._client import Nyaa
from ._enums import Category, Filter, Order, ParentCategory, SortBy
from ._errors import BencodeError, ParsingError, PyNyaaError, ReleaseNotFoundError
from ._models import File, NyaaRelease, Submitter, Torrent
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


def __dir__() -> list[str]:  # pragma: no cover
    return list(__all__)


__all__: Final = (
    "AsyncNyaa",
    "BencodeError",
    "Category",
    "File",
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
    "Torrent",
    "__version__",
    "get",
    "search",
)
