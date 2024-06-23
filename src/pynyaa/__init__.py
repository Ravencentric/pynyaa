from httpx import HTTPStatusError
from pydantic import ValidationError

from ._clients import AsyncNyaa, Nyaa
from ._enums import NyaaCategory
from ._models import NyaaTorrentPage
from ._version import Version, _get_version

__version__ = _get_version()
__version_tuple__ = Version(*tuple(map(int, __version__.split("."))))

__all__ = [
    # Clients
    "AsyncNyaa",
    "Nyaa",
    # Enums
    "NyaaCategory",
    # Models
    "NyaaTorrentPage",
    # Exceptions
    "HTTPStatusError",
    "ValidationError",
]
