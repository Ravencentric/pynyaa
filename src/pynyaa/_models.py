from __future__ import annotations

from datetime import datetime

from pydantic import AnyUrl, BaseModel, ConfigDict, HttpUrl, field_validator
from torf import Torrent

from ._enums import NyaaCategory


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

    magnet: AnyUrl
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

    @field_validator("information")
    @classmethod
    def replace_empty_info_with_none(cls, information: str) -> str | None:
        """
        If the information field is empty, Nyaa replaces it with a placeholder value.
        This replaces said placeholder value with `None`.
        """
        if information == "No information.":
            return None
        return information

    @field_validator("description")
    @classmethod
    def replace_empty_desc_with_none(cls, description: str) -> str | None:
        """
        If the description field is empty, Nyaa replaces it with a placeholder value.
        This replaces said placeholder value with `None`.
        """
        if description == "#### No description.":
            return None
        return description


__all__ = [
    "Submitter",
    "NyaaTorrentPage",
]
