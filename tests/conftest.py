# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from httpx import AsyncClient, Client

from pynyaa import AsyncNyaa, Nyaa

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # Since the sync tests are generated from the async tests,
    # they make identical requests from identically named test functions.
    # This means we can share a single response per two test functions (sync and async)
    #
    # This simply checks for an existing pytest.mark.vcr and then applies
    # pytest.mark.default_cassette on top.
    for item in items:
        if item.get_closest_marker("vcr") is not None and item.get_closest_marker("default_cassette") is None:
            path = Path(__file__).parent / "cassettes" / f"{item.name}.yaml"
            item.add_marker(pytest.mark.default_cassette(str(path)))


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Any]:
    return {
        "filter_headers": ["cookie"],
        "before_record_response": lambda response: {
            **response,
            "headers": {key: value for key, value in response["headers"].items() if key.lower() != "set-cookie"},
        },
    }


@pytest.fixture
def nyaa_client() -> Iterator[Nyaa]:
    with Nyaa(client=Client(headers=headers, timeout=30)) as nyaa:
        yield nyaa


@pytest.fixture
async def async_nyaa_client() -> AsyncIterator[AsyncNyaa]:
    async with AsyncNyaa(client=AsyncClient(headers=headers, timeout=30)) as nyaa:
        yield nyaa
