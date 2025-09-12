from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as dt

    from ._enums import Category


@dataclass(frozen=True, kw_only=True, slots=True)
class TorrentFile:
    """Represents a torrent file, including its associated data and metadata."""

    name: str
    """The name of the torrent."""
    data: bytes
    """The raw data of the torrent file."""
    size: int
    """The size of the torrent in bytes."""
    infohash: str
    """The infohash of the torrent."""
    url: str
    """The URL to the torrent file."""
    magnet: str
    """The magnet link for the torrent."""

    def __str__(self) -> str:
        return self.name


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


@dataclass(frozen=True, kw_only=True, slots=True)
class NyaaTorrentPage:
    """Represents a specific torrent's page on Nyaa."""

    id: int
    """The Nyaa ID of the torrent (e.g., `https://nyaa.si/view/{id}`)."""

    url: str
    """The URL to the Nyaa torrent page (e.g., `https://nyaa.si/view/123456`)."""

    title: str
    """The title of the torrent."""

    category: Category
    """The torrent's category."""

    submitter: Submitter | None
    """
    The user who submitted the torrent.
    This is `None` if the submitter is anonymous.
    """

    datetime: dt.datetime
    """The date and time at which the torrent was submitted."""

    information: str | None
    """Additional information about the torrent."""

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
    An upload can be both trusted and a remake. In this case, the remake
    status takes priority, so `is_remake` will be `True` and `is_trusted` will be `False`.
    """

    is_remake: bool
    """
    Indicates whether the upload is a remake (red) or not.

    Note
    ----
    An upload can be both trusted and a remake. In this case, the remake
    status takes priority, so `is_remake` will be `True` and `is_trusted` will be `False`.
    """

    torrent: TorrentFile
    """The `.torrent` file associated with this page."""

    description: str | None
    """The torrent's description."""

    def __str__(self) -> str:
        return self.title
