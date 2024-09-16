from pydantic import AnyUrl, UrlConstraints
from typing_extensions import Annotated

MagnetUrl = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["magnet"])]
"""Url that only allows magnets."""
