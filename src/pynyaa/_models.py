# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as dt

    from ._enums import Category


@dataclass(frozen=True, kw_only=True, slots=True)
class Submitter:
    """Represents the user who submitted the torrent."""

    name: str
    """The username of the submitter."""
    url: str
    """The profile URL of the submitter."""
    is_trusted: bool
    """Indicates whether the user is trusted (green) or not."""
    is_banned: bool
    """Indicates whether the user is banned or not."""

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True, init=False)
class File:
    """Represents a file in the torrent."""

    # We cannot use PurePosixPath directly
    # because it offers additional functionality
    # which is either nonsensical or ambiguous for
    # our use case.
    _inner: tuple[PurePosixPath, int] = field(init=False)  # https://github.com/facebook/pyrefly/issues/5326

    def __init__(self, path: str, /, *, size: int) -> None:
        object.__setattr__(self, "_inner", (PurePosixPath(path), size))

    @property
    def name(self) -> str:
        """The final path component, if any, following `pathlib` semantics."""
        path, _ = self._inner
        return path.name

    @property
    def stem(self) -> str:
        """The final path component, minus its last suffix, following `pathlib` semantics."""
        path, _ = self._inner
        return path.stem

    @property
    def suffix(self) -> str:
        """
        The final component's last suffix, if any, following `pathlib` semantics.
        This includes the leading period. For example: '.txt'
        """
        path, _ = self._inner
        return path.suffix

    @property
    def size(self) -> int:
        """The exact size of the file, in bytes."""
        _, size = self._inner
        return size

    def __str__(self) -> str:
        path, _ = self._inner
        return str(path)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self)!r}, size={self.size!r})"

    def __fspath__(self) -> str:
        path, _ = self._inner
        return str(path)


@dataclass(frozen=True, kw_only=True, slots=True)
class Torrent:
    """Represents the torrent attached to the release."""

    name: str
    """The name of the content described by the torrent."""
    filename: str
    """The filename of the `.torrent` file itself."""
    files: tuple[File, ...]
    """The files included in the torrent, in the order they're listed."""
    data: bytes = field(repr=False)
    """The raw contents of the `.torrent` file."""
    infohash: str
    """The infohash of the torrent."""
    url: str
    """The URL pointing to the torrent file."""
    magnet: str
    """The magnet link for the torrent."""

    @property
    def size(self) -> int:
        """
        The total size of the torrent's payload in bytes.

        This is the combined size of all files contained in the torrent,
        not the size of the `.torrent` file itself. For example, a 20 KB
        `.torrent` file describing a 2 GB download would have a `size`
        of 2 GB. To get the size of the `.torrent` file instead, use
        `len(data)`.
        """
        return sum(file.size for file in self.files)

    def __str__(self) -> str:
        return self.filename


@dataclass(frozen=True, kw_only=True, slots=True)
class NyaaRelease:
    """Represents a specific release (torrent) on Nyaa."""

    id: int
    """The Nyaa ID of the release (e.g., `https://nyaa.si/view/{id}`)."""

    url: str
    """The URL pointing to the Nyaa release page (e.g., `https://nyaa.si/view/123456`)."""

    title: str
    """The title of the release."""

    category: Category
    """The release's category."""

    submitter: Submitter | None
    """
    The user who submitted the release.
    This is `None` if the submitter is anonymous.
    """

    submitted_at: dt.datetime
    """When the release was submitted to Nyaa, in UTC."""

    information: str | None
    """Additional information about the release."""

    seeders: int = field(compare=False)
    """The number of seeders."""

    leechers: int = field(compare=False)
    """The number of leechers."""

    completed: int = field(compare=False)
    """The number of completed downloads."""

    is_trusted: bool
    """
    Indicates whether the upload is trusted (green) or not.

    Note
    ----
    A release can be both trusted and a remake. In this case, the remake
    status takes priority, so `is_remake` will be `True` and `is_trusted` will be `False`.
    """

    is_remake: bool
    """
    Indicates whether the upload is a remake (red) or not.

    Note
    ----
    A release can be both trusted and a remake. In this case, the remake
    status takes priority, so `is_remake` will be `True` and `is_trusted` will be `False`.
    """

    torrent: Torrent
    """The torrent associated with this release, including its files and metadata."""

    description: str | None
    """The release's description."""

    def __str__(self) -> str:
        return self.title
