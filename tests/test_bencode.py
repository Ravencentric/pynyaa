from __future__ import annotations

from pathlib import Path

import pytest

from pynyaa import BencodeError, PyNyaaError
from pynyaa._bencode import _decode, parse_torrent_size


@pytest.mark.parametrize(
    ("data", "message"),
    [
        (b"-3:a", "Negative byte string length"),
        (b"d1:xe", "Dictionary has an unmatched key"),
        (b"10:abc", "Truncated byte string"),
    ],
    ids=["negative-length", "unmatched-key", "truncated-string"],
)
def test_decode_invalid(data: bytes, message: str) -> None:
    with pytest.raises(BencodeError, match=message):
        _decode(data)


@pytest.mark.parametrize("data", [b"iXe", b"li1e", b"dli1eei2ee"])
def test_decode_errors_are_pynyaa_errors(data: bytes) -> None:
    with pytest.raises(PyNyaaError) as caught:
        _decode(data)
    assert isinstance(caught.value, BencodeError)


def test_decode_single_file() -> None:
    torrent = Path(__file__).parent / "fixtures" / "torrents" / "single-file.torrent"
    assert _decode(torrent.read_bytes()) == {
        b"comment": b"6:lengthi999e",
        b"info": {
            b"length": 61_957,
            b"name": b"single.bin",
            b"piece length": 16_384,
            b"pieces": bytes.fromhex("80cb9c430d80c3084649f65e0ca25dabbffb1b62") * 3
            + bytes.fromhex("169888128712e814b8409606e8d2c84493bb51e7"),
        },
    }


def test_decode_multi_file() -> None:
    torrent = Path(__file__).parent / "fixtures" / "torrents" / "multi-file.torrent"
    assert _decode(torrent.read_bytes()) == {
        b"comment": b"6:lengthi999e",
        b"info": {
            b"files": [
                {b"length": 65_537, b"path": [b"a.bin"]},
                {b"length": 0, b"path": [b"empty.bin"]},
                {b"length": 119, b"path": [b"nested", b"b.bin"]},
                {b"length": 1_413, b"path": [b"nested", "\u65e5\u672c.txt".encode()]},
            ],
            b"name": b"multiple",
            b"piece length": 16_384,
            b"pieces": bytes.fromhex("7db67baceeecb3a420bf37a7beca4a45185f8f3c") * 4
            + bytes.fromhex("6c2a3989921e229b432be48f00b55b8bc3a70623"),
        },
    }


def test_decode_single_file_directory() -> None:
    torrent = Path(__file__).parent / "fixtures" / "torrents" / "single-file-directory.torrent"
    assert _decode(torrent.read_bytes()) == {
        b"comment": b"6:lengthi999e",
        b"info": {
            b"files": [{b"length": 257, b"path": [b"payload.bin"]}],
            b"name": b"one-file",
            b"piece length": 16_384,
            b"pieces": bytes.fromhex("4f88e8f888069d9d8f0e141fb24ad6dbdd4f5959"),
        },
    }


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"d4:infod6:lengthi619580447eee", 619580447),
        (b"d4:infod5:filesld6:lengthi100eed6:lengthi200eeeee", 300),
        (b"d4:infod6:lengthi0eee", 0),
        (b"d4:infod5:filesleee", 0),
        (b"d4:infod5:filesld6:lengthi100eee6:lengthi999eee", 100),
        (b"d4:infod6:lengthi123eee4:spam", 123),
        (b"d4:infod6:lengthi00123eee", 123),
    ],
    ids=[
        "single-file",
        "multi-file",
        "empty-file",
        "empty-files",
        "files-precedence",
        "trailing-data",
        "leading-zeros",
    ],
)
def test_parse_torrent_size(data: bytes, expected: int) -> None:
    assert parse_torrent_size(data) == expected


def test_parse_torrent_size_ignores_other_metadata() -> None:
    decoy = b"6:lengthi999e"
    encoded_decoy = str(len(decoy)).encode() + b":" + decoy
    data = (
        b"d7:comment"
        + encoded_decoy
        + b"5:extrald6:lengthi999eee"
        + b"4:infod6:lengthi123e6:pieces"
        + encoded_decoy
        + b"ee"
    )
    assert parse_torrent_size(data) == 123
