from __future__ import annotations


class PyNyaaError(Exception):
    """Base exception for all pynyaa errors."""

    __module__ = "pynyaa"

    def __init_subclass__(cls) -> None:
        # Ensure subclasses also appear as part of the public 'pynyaa' module
        # in tracebacks, instead of the internal implementation module.
        cls.__module__ = "pynyaa"


class ParsingError(PyNyaaError):
    """Raised when there is an error parsing the HTML."""


class ReleaseNotFoundError(PyNyaaError):
    """Raised when the requested release cannot be found on Nyaa."""

    def __init__(self, url: str):
        super().__init__(
            f"Release not found at {url!r}\nIt may have been removed, never existed, or the ID/URL is incorrect."
        )
