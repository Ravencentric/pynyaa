from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._errors import BencodeError

if TYPE_CHECKING:
    from collections.abc import Mapping


def bendecode(data: bytes) -> Mapping[bytes, Any]:
    """Decode a torrent's bencoded metadata, preserving byte strings as bytes."""

    def read(index: int) -> tuple[Any, int]:
        """Return the decoded value and the byte offset immediately after it."""
        match data[index : index + 1]:
            case b"i":
                # Integers use i<number>e, for example i42e.
                end = data.index(b"e", index + 1)
                return int(data[index + 1 : end]), end + 1

            case b"l" | b"d" as token:
                items: list[Any] = []
                index += 1  # Skip the opening l or d.
                # Nested reads consume their own terminators, leaving this container's e.
                while data[index : index + 1] != b"e":
                    item, index = read(index)
                    items.append(item)
                if token == b"l":
                    return items, index + 1
                if len(items) % 2:
                    raise BencodeError("Dictionary has an unmatched key.")
                # Dictionary entries alternate between keys and values.
                return dict(zip(items[::2], items[1::2])), index + 1

            case _:
                # Byte strings use <length>:<raw bytes>. Their contents can include i, l, d, or e.
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
        value: Mapping[bytes, Any] = read(0)[0]
    except (ValueError, TypeError, RecursionError) as error:
        raise BencodeError(str(error)) from error

    return value
