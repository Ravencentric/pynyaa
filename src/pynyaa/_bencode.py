"""Decode bencoded torrent metadata and read its payload size."""

from __future__ import annotations

from typing import Any

from ._errors import BencodeError

# Decoder adapted from https://github.com/utdemir/bencoder (CC0-1.0).


def _decode(data: bytes) -> Any:
    def read(index: int) -> tuple[Any, int]:
        match data[index : index + 1]:
            case b"i":
                end = data.index(b"e", index + 1)
                return int(data[index + 1 : end]), end + 1
            case b"l" | b"d" as token:
                items: list[Any] = []
                index += 1
                while data[index : index + 1] != b"e":
                    item, index = read(index)
                    items.append(item)
                if token == b"l":
                    return items, index + 1
                if len(items) % 2:
                    raise BencodeError("Dictionary has an unmatched key.")
                return dict(zip(items[::2], items[1::2])), index + 1
            case _:
                colon = data.index(b":", index)
                length = int(data[index:colon])
                if length < 0:
                    raise BencodeError("Negative byte string length.")
                start = colon + 1
                end = start + length
                if end > len(data):
                    raise BencodeError("Truncated byte string.")
                return data[start:end], end

    try:
        value, _ = read(0)
    except (ValueError, TypeError, RecursionError) as error:
        raise BencodeError(str(error)) from error
    return value


def parse_torrent_size(data: bytes) -> int:
    """Return the total payload size in bytes from a torrent's info dictionary."""
    info = _decode(data)[b"info"]
    if (files := info.get(b"files")) is not None:
        return sum(file[b"length"] for file in files)
    length: int = info[b"length"]
    return length
