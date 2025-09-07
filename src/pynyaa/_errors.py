from __future__ import annotations


class PyNyaaError(Exception):
    """Base exception for all pynyaa errors."""


class ParsingError(PyNyaaError):
    """Raised when there is an error parsing the HTML."""


class TorrentNotFoundError(PyNyaaError):
    """Raised when the requested torrent page cannot be found on Nyaa."""

    def __init__(self, url: str):
        super().__init__(
            f"Torrent not found at {url!r}\nIt may have been removed, never existed, or the ID/URL is incorrect."
        )
