from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator
from torf import Torrent

from ._enums import NyaaCategory
from ._types import MagnetUrl


class ParentModel(BaseModel):
    """
    Parent model that stores global configuration
    All models ahead will inherit from this.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class Submitter(ParentModel):
    """User who submitted the torrent."""

    name: str
    """Username of the submitter."""
    url: HttpUrl
    """Profile URL of the submitter."""
    is_trusted: bool
    """Indicates whether the user is trusted (green) or not."""
    is_banned: bool
    """Indicates whether the user is banned or not."""

    def __eq__(self, other: object) -> bool:
        """
        Implements equality method.
        Two Submitter(s) are equal if they both point to the same URL.
        """
        if not isinstance(other, Submitter):
            return NotImplemented
        return self.url == other.url

    def __hash__(self) -> int:
        """
        Makes Submitter hashable.
        """
        return self.url.__hash__()
    
    def __repr__(self) -> str:
        """
        This matches Submitter's repr with NyaaTorrentPage's for consistency.
        """
        return f"{self.__class__.__name__}(name='{self.name}', url='{self.url}', is_trusted={self.is_trusted}, is_banned={self.is_banned})"

    def __str__(self) -> str:
        """
        Same as __repr___.
        """
        return repr(self)


class NyaaTorrentPage(ParentModel):
    """Nyaa's torrent page."""

    id: int
    """Nyaa ID of the torrent (`https://nyaa.si/view/{id}`)."""

    url: HttpUrl
    """URL to the Nyaa torrent page (`https://nyaa.si/view/123456`)."""

    title: str
    """Title of the torrent."""

    category: NyaaCategory
    """Torrent category."""

    date: datetime
    """Date and time at which the torrent was submitted."""

    submitter: Submitter
    """User who submitted the torrent."""

    information: str | None
    """Information about the torrent."""

    seeders: int
    """Number of seeders."""

    leechers: int
    """Number of leechers."""

    completed: int
    """Number of completed downloads."""

    is_trusted: bool
    """Indicates whether the upload is trusted (green) or not."""

    is_remake: bool
    """
    Indicates whether the upload is a remake (red) or not.
    
    Note
    ----
    An upload can be both trusted and a remake, in which case,
    the remake takes priority, that is, `is_remake` will be `True`
    and `is_trusted` will be `False`.
    This is a current limitation that I don't know how to work around.
    """

    description: str | None
    """Torrent description."""

    torrent_file: HttpUrl
    """URL pointing to the `.torrent` file (`https://nyaa.si/download/123456.torrent`)"""

    magnet: MagnetUrl
    """
    Magnet link of the torrent. 
    
    Note
    ----
    The magnet link provided by Nyaa is different from the one 
    you'll get if you simply generated it from the `.torrent` file itself
    because Nyaa strips away all trackers except it's own 
    and the ones listed [here](https://github.com/nyaadevs/nyaa/blob/master/trackers.txt).
    """

    torrent: Torrent
    """
    A [`torf.Torrent`](https://torf.readthedocs.io/en/latest/#torf.Torrent) object 
    representing the data stored in the `.torrent` file.
    """

    @field_validator("information", "description")
    @classmethod
    def _replace_placeholder(cls, placeholder: str) -> str | None:
        """
        If the information or description field is empty, Nyaa replaces it with a placeholder value.
        This replaces said placeholder value with `None`.
        """
        if placeholder in ("No information.", "#### No description."):
            return None
        return placeholder

    def __eq__(self, other: object) -> bool:
        """
        Implements equality method.
        Two NyaaTorrentPage(s) are equal if they both point to the same URL.
        """
        if not isinstance(other, NyaaTorrentPage):
            return NotImplemented
        return self.url == other.url

    def __hash__(self) -> int:
        """
        Makes NyaaTorrentPage hashable.
        """
        return self.url.__hash__()
    
    def __repr__(self) -> str:
        """
        A shorter human readable __repr__ because
        the default one is too long.
        """
        return f"{self.__class__.__name__}(title='{self.title}', url='{self.url}', date='{self.date.isoformat()}', submitter='{self.submitter.name}')"

    def __str__(self) -> str:
        """
        Same as __repr__
        """
        return repr(self)
