from pydantic import AnyUrl, Field, UrlConstraints
from typing_extensions import Annotated

SearchLimit = Annotated[int, Field(gt=0, le=75)]
"""Integer with lower and upper limits."""

MagnetUrl = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["magnet"])]
"""Url that only allows magnets."""
