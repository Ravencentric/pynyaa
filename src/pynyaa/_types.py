"""
Aside from providing it's own types, this module also re-exports the following for convenience:
- [AnyUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.AnyUrl)
- [HttpUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl)
- [Torrent](https://torf.readthedocs.io/en/latest/#torf.Torrent)
- [File](https://torf.readthedocs.io/en/latest/#torf.File)
- [Filepath](https://torf.readthedocs.io/en/latest/#torf.Filepath)
"""

from __future__ import annotations

from typing import Any

from pydantic import AnyUrl, HttpUrl
from torf import File, Filepath, Torrent
from typing_extensions import TypeAlias

HTTPXClientKwargs: TypeAlias = Any
"""Simple TypeAlias to refer to `httpx.Client()` kwargs"""

HTTPXAsyncClientKwargs: TypeAlias = Any
"""Simple TypeAlias to refer to `httpx.AsyncClient()` kwargs"""

__all__ = [
    "AnyUrl",
    "HttpUrl",
    "HTTPXAsyncClientKwargs",
    "HTTPXClientKwargs",
    "Torrent",
    "File",
    "Filepath",
]
