# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import pytest

from pynyaa._parser import parse_release_id


@pytest.mark.parametrize(
    "page",
    [
        123,
        "https://nyaa.si/view/123",
        "http://nyaa.si/view/123",
        "https://sukebei.nyaa.si/view/123",
        "https://nyaa.si/view/123/",
        "https://nyaa.si/view/123?ref=example",
        "https://nyaa.si/view/123#comments",
        "https://nyaa.si/view/123?",
        "https://nyaa.si/view/123#",
        "https://nyaa.si/view/123/?ref=example#comments",
        "https://nyaa.si/download/123",
        "ftp://nyaa.si/view/123",
        "//nyaa.si/view/123",
        "https://example.com/123",
    ],
)
def test_parse_release_id(page: int | str) -> None:
    assert parse_release_id(page) == 123


@pytest.mark.parametrize(
    "page",
    [
        "123",
        "/view/123",
        "nyaa.si/view/123",
        "https://nyaa.si/view/",
        "https:///view/123",
        "https://nyaa.si/view/123/extra",
    ],
)
def test_parse_release_id_requires_release_url(page: str) -> None:
    with pytest.raises(ValueError):
        parse_release_id(page)


@pytest.mark.parametrize("id", ["+123", "-123", "1_23", " 123", "123 ", "12abc"])
def test_parse_release_id_requires_digits(id: str) -> None:
    with pytest.raises(ValueError):
        parse_release_id(f"https://nyaa.si/view/{id}")


def test_parse_release_id_requires_int_or_str() -> None:
    with pytest.raises(TypeError, match="Parameter 'page' expected 'int' or 'str', but got 'NoneType'."):
        parse_release_id(None)  # type: ignore[arg-type]
