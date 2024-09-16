from httpx import HTTPStatusError

from pynyaa._clients._async import AsyncNyaa
from pynyaa._clients._sync import Nyaa
from pynyaa._enums import NyaaCategory, NyaaFilter
from pynyaa._models import NyaaTorrentPage, Submitter
from pynyaa._version import __version__, __version_tuple__

__all__ = (
    # Clients
    "AsyncNyaa",
    "Nyaa",
    # Enums
    "NyaaCategory",
    "NyaaFilter",
    # Models
    "NyaaTorrentPage",
    "Submitter",
    # Exceptions
    "HTTPStatusError",
    # Version
    "__version__",
    "__version_tuple__",
)
