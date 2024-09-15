from httpx import HTTPStatusError

from pynyaa._clients._async import AsyncNyaa
from pynyaa._clients._sync import Nyaa
from pynyaa._enums import NyaaCategory, NyaaFilter
from pynyaa._models import NyaaTorrentPage, Submitter
from pynyaa._version import Version, _get_version

__version__ = _get_version()
__version_tuple__ = Version(*[int(i) for i in __version__.split(".")])

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
)
