from __future__ import annotations

import pytest
from httpx import Client
from typing_extensions import Generator

from pynyaa import Nyaa


@pytest.fixture
def nyaa_client() -> Generator[Nyaa]:
    nyaa = Nyaa(
        client=Client(
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            }
        )
    )

    yield Nyaa
    nyaa.close()
