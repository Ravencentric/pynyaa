from __future__ import annotations

from typing import TYPE_CHECKING

from platformdirs import user_cache_path

if TYPE_CHECKING:
    from pathlib import Path


def _get_user_cache_path() -> Path:
    return user_cache_path(appname="pynaa", ensure_exists=True)
