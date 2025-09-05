from __future__ import annotations


class PyNyaaError(Exception):
    """Base exception for all pynyaa errors."""

    pass


class ParsingError(PyNyaaError):
    """Raised when there is an error parsing the HTML."""

    pass


class TorrentNotFoundError(PyNyaaError):
    """Raised when a torrent is not found."""

    pass
