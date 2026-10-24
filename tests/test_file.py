from __future__ import annotations

from pathlib import Path

from pynyaa import File


def test_file() -> None:
    file = File("Release/Subs/English.ass", size=1234)

    assert str(file) == "Release/Subs/English.ass"
    assert file.name == "English.ass"
    assert file.stem == "English"
    assert file.suffix == ".ass"
    assert file.size == 1234


def test_file_works_with_pathlike_consumers() -> None:
    file = File("Release/Subs/English.ass", size=1234)

    assert Path("downloads") / file == Path("downloads", "Release", "Subs", "English.ass")
