from __future__ import annotations

from typing import TYPE_CHECKING

from platformdirs import user_cache_path

if TYPE_CHECKING:  # pragma: no cover
    from pathlib import Path


def get_user_cache_path() -> Path:
    return user_cache_path(appname="pynyaa", ensure_exists=True).resolve()
