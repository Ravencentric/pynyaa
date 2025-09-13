from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from httpx import AsyncClient, Client

from pynyaa import AsyncNyaa, Nyaa

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


@pytest.fixture
def nyaa_client() -> Iterator[Nyaa]:
    with Nyaa(client=Client(headers=headers)) as nyaa:
        yield nyaa


@pytest.fixture
async def async_nyaa_client() -> AsyncIterator[AsyncNyaa]:
    async with AsyncNyaa(client=AsyncClient(headers=headers)) as nyaa:
        yield nyaa
