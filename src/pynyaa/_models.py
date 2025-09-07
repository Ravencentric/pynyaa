from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as dt

    from pynyaa._enums import Category


@dataclass(frozen=True, kw_only=True, slots=True)
class Submitter:
    """Represents the user who submitted the torrent."""

    name: str
    """Username of the submitter."""
    url: str
    """Profile URL of the submitter."""
    is_trusted: bool
    """Indicates whether the user is trusted (green) or not."""
    is_banned: bool
    """Indicates whether the user is banned or not."""


@dataclass(frozen=True, kw_only=True, slots=True)
class NyaaTorrentPage:
    """Represents Nyaa's torrent page."""

    id: int
    """Nyaa ID of the torrent (`https://nyaa.si/view/{id}`)."""

    url: str
    """URL to the Nyaa torrent page (`https://nyaa.si/view/123456`)."""

    title: str
    """Title of the torrent."""

    category: Category
    """Torrent category."""

    submitter: Submitter | None
    """
    User who submitted the torrent.
    This will be `None` if the submitter is anonymous.
    """

    datetime: dt.datetime
    """Date and time at which the torrent was submitted."""

    information: str | None
    """Information about the torrent."""

    seeders: int
    """Number of seeders."""

    leechers: int
    """Number of leechers."""

    completed: int
    """Number of completed downloads."""

    size: int
    """Size of the torrent."""

    infohash: str
    """Info hash of the torrent."""

    is_trusted: bool
    """
    Indicates whether the upload is trusted (green) or not.

    Note
    ----
    An upload can be both trusted and a remake, in which case,
    the remake takes priority, that is, `is_remake` will be `True`
    and `is_trusted` will be `False`.
    """

    is_remake: bool
    """
    Indicates whether the upload is a remake (red) or not.

    Note
    ----
    An upload can be both trusted and a remake, in which case,
    the remake takes priority, that is, `is_remake` will be `True`
    and `is_trusted` will be `False`.
    """

    description: str | None
    """Torrent description."""

    torrent: str
    """URL pointing to the `.torrent` file (`https://nyaa.si/download/123456.torrent`)"""

    magnet: str
    """
    Magnet link of the torrent.

    Note
    ----
    The magnet link provided by Nyaa is different from the one
    you'll get if you simply generated it from the `.torrent` file itself
    because Nyaa strips away all trackers except it's own
    and the ones listed [here](https://github.com/nyaadevs/nyaa/blob/master/trackers.txt).
    """
