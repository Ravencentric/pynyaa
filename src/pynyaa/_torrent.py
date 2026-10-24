from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import unquote

from ._bencode import bendecode
from ._errors import BencodeError
from ._models import File

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any


class TorrentParser:
    __slots__ = ("_encoding", "_info")

    def __init__(self, *, data: bytes) -> None:
        metadata = bendecode(data)
        self._info: Mapping[bytes, Any] = metadata[b"info"]

        # Nyaa decodes stuff using the declared encoding, defaulting to UTF-8.
        # https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/nyaa/forms.py#L567-L571
        self._encoding: str = metadata.get(b"encoding", b"utf-8").decode("utf-8")

    def name(self) -> str:
        # Nyaa prefers `{key}.utf-8` over `{key}`.
        # https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/nyaa/backend.py#L60-L73
        # https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/tests/test_backend.py#L19
        try:
            if (name := self._info.get(b"name.utf-8")) is not None:
                name: str = name.decode("utf-8")
            else:
                name: str = self._info[b"name"].decode(self._encoding)
        except KeyError as error:
            raise BencodeError("Torrent info must contain a name and either files or length.") from error

        return name

    def files(self) -> tuple[File, ...]:
        name = self.name()

        if (files := self._info.get(b"files")) is not None:
            entries: list[File] = []
            for file in files:
                if (parts := file.get(b"path.utf-8")) is not None:
                    parts: list[str] = [part.decode("utf-8") for part in parts]
                else:
                    parts: list[str] = [part.decode(self._encoding) for part in file[b"path"]]

                # If the last value is empty, then it's a "bitcomet directory"
                # which Nyaa ignores as a file.
                # https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/nyaa/backend.py#L288-L296
                if parts[-1] == "":
                    continue

                path = "/".join((name, *parts))
                size = file[b"length"]
                entries.append(File(path, size=size))

            return tuple(entries)

        try:
            size = self._info[b"length"]
        except KeyError as error:
            raise BencodeError("Torrent info must contain a name and either files or length.") from error

        return (File(name, size=size),)


def parse_torrent_filename(content_disposition: str) -> str:
    """
    Return the decoded filename from a [`Content-Disposition`][0] header
    as used by [`Nyaa`][1].

    [0]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
    [1]: https://github.com/nyaadevs/nyaa/blob/4fe0ff5b1aa7ec7c9bb2667d97e10ce2a318c676/nyaa/views/torrents.py#L316-L335
    """
    _, filename = content_disposition.split("filename*=UTF-8''")
    return unquote(filename)
