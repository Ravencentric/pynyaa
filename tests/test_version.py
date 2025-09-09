from __future__ import annotations

import tomli

from pynyaa import __version__


def test_versions_match() -> None:
    with open("pyproject.toml", "rb") as f:
        assert tomli.load(f)["project"]["version"] == __version__
