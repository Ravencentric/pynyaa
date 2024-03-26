from ._clients import AsyncNyaa, Nyaa
from ._enums import NyaaCategory
from ._exceptions import (
    CloseError,
    ConnectError,
    ConnectTimeout,
    CookieConflict,
    DecodingError,
    HTMLParsingError,
    HTTPError,
    HTTPStatusError,
    InvalidURL,
    LocalProtocolError,
    NetworkError,
    PoolTimeout,
    ProtocolError,
    ProxyError,
    ReadError,
    ReadTimeout,
    RemoteProtocolError,
    RequestError,
    RequestNotRead,
    ResponseNotRead,
    StreamClosed,
    StreamConsumed,
    StreamError,
    TimeoutException,
    TooManyRedirects,
    UnsupportedProtocol,
    ValidationError,
    WriteError,
    WriteTimeout,
)
from ._models import NyaaTorrentPage
from ._types import AnyUrl, File, Filepath, HttpUrl, Torrent
from ._version import _get_version

__version__ = _get_version()
__version_tuple__ = tuple(__version__.split("."))

__all__ = [
    # Clients
    "AsyncNyaa",
    "Nyaa",
    # Enums
    "NyaaCategory",
    # Types
    "AnyUrl",
    "HttpUrl",
    "Torrent",
    "File",
    "Filepath",
    # Models
    "NyaaTorrentPage",
    # Exceptions
    "CloseError",
    "ConnectError",
    "ConnectTimeout",
    "CookieConflict",
    "DecodingError",
    "HTMLParsingError",
    "HTTPError",
    "HTTPStatusError",
    "InvalidURL",
    "LocalProtocolError",
    "NetworkError",
    "PoolTimeout",
    "ProtocolError",
    "ProxyError",
    "ReadError",
    "ReadTimeout",
    "RemoteProtocolError",
    "RequestError",
    "RequestNotRead",
    "ResponseNotRead",
    "StreamClosed",
    "StreamConsumed",
    "StreamError",
    "TimeoutException",
    "TooManyRedirects",
    "UnsupportedProtocol",
    "WriteError",
    "WriteTimeout",
    "ValidationError",
]
