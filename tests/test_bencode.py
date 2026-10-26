# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from pynyaa import BencodeError
from pynyaa._bencode import bendecode


def bendecoded(name: str) -> Mapping[bytes, Any]:
    p = Path(__file__).parent / "fixtures" / "torrents" / name
    b = p.read_bytes()
    return bendecode(b)


@pytest.mark.parametrize(
    ("data", "message"),
    [
        (b"-3:a", "Negative byte string length"),
        (b"d1:xe", "Dictionary has an unmatched key"),
        (b"10:abc", "Truncated byte string"),
        (b"d1:xiabcee", "invalid literal for int"),
    ],
    ids=["negative-length", "unmatched-key", "truncated-string", "invalid-integer"],
)
def test_decode_invalid(data: bytes, message: str) -> None:
    with pytest.raises(BencodeError, match=message):
        bendecode(data)


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        pytest.param(
            "single-file.torrent",
            {
                b"comment": b"6:lengthi999e",
                b"info": {
                    b"length": 61_957,
                    b"name": b"single.bin",
                    b"piece length": 16_384,
                    b"pieces": (
                        bytes.fromhex("80cb9c430d80c3084649f65e0ca25dabbffb1b62") * 3
                        + bytes.fromhex("169888128712e814b8409606e8d2c84493bb51e7")
                    ),
                },
            },
            id="single-file",
        ),
        pytest.param(
            "multi-file.torrent",
            {
                b"comment": b"6:lengthi999e",
                b"info": {
                    b"files": [
                        {b"length": 65_537, b"path": [b"a.bin"]},
                        {b"length": 0, b"path": [b"empty.bin"]},
                        {b"length": 119, b"path": [b"nested", b"b.bin"]},
                        {
                            b"length": 1_413,
                            b"path": [b"nested", "\u65e5\u672c.txt".encode()],
                        },
                    ],
                    b"name": b"multiple",
                    b"piece length": 16_384,
                    b"pieces": (
                        bytes.fromhex("7db67baceeecb3a420bf37a7beca4a45185f8f3c") * 4
                        + bytes.fromhex("6c2a3989921e229b432be48f00b55b8bc3a70623")
                    ),
                },
            },
            id="multi-file",
        ),
    ],
)
def test_decode(filename: str, expected: Mapping[bytes, Any]) -> None:
    assert bendecoded(filename) == expected
