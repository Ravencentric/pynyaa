from __future__ import annotations

from pathlib import Path

import pytest

from pynyaa import BencodeError, File
from pynyaa._torrent import TorrentParser, parse_torrent_filename


def test_torrent_download_filename() -> None:
    header = "attachment; filename*=UTF-8''%E6%97%A5%E6%9C%AC%20%2B%20subs.torrent"
    assert parse_torrent_filename(header) == "日本 + subs.torrent"


@pytest.mark.parametrize(
    ("fixture", "name", "files"),
    [
        pytest.param(
            "single-file.torrent",
            "single.bin",
            (File("single.bin", size=61_957),),
            id="single-file",
        ),
        pytest.param(
            "multi-file.torrent",
            "multiple",
            (
                File("multiple/a.bin", size=65_537),
                File("multiple/empty.bin", size=0),
                File("multiple/nested/b.bin", size=119),
                File("multiple/nested/日本.txt", size=1_413),
            ),
            id="multi-file",
        ),
        pytest.param(
            "single-file-directory.torrent",
            "one-file",
            (File("one-file/payload.bin", size=257),),
            id="single-file-directory",
        ),
    ],
)
def test_torrent(fixture: str, name: str, files: tuple[File, ...]) -> None:
    data = (Path(__file__).parent / "fixtures" / "torrents" / fixture).read_bytes()
    parser = TorrentParser(data=data)
    assert parser.name() == name
    assert parser.files() == files


@pytest.mark.parametrize(
    ("data", "name", "files"),
    [
        pytest.param(
            b"d8:encoding6:cp12524:infod6:lengthi7e4:name8:caf\xe9.mkvee",
            "café.mkv",
            (File("café.mkv", size=7),),
            id="single-file-declared-encoding",
        ),
        pytest.param(
            b"d8:encoding6:cp12524:infod5:filesld6:lengthi7e4:pathl4:Subs8:caf\xe9.mkveee4:name4:caf\xe9ee",
            "café",
            (File("café/Subs/café.mkv", size=7),),
            id="multi-file-declared-encoding",
        ),
        pytest.param(
            b"d8:encoding6:cp12524:infod6:lengthi7e4:name10:legacy.mkv10:name.utf-89:caf\xc3\xa9.mkvee",
            "café.mkv",
            (File("café.mkv", size=7),),
            id="single-file-utf8-override",
        ),
        pytest.param(
            b"d8:encoding6:cp12524:infod5:filesl"
            b"d6:lengthi7e4:pathl10:legacy.mkve10:path.utf-8l4:Subs9:caf\xc3\xa9.mkveee"
            b"4:name6:legacy10:name.utf-85:caf\xc3\xa9ee",
            "café",
            (File("café/Subs/café.mkv", size=7),),
            id="multi-file-utf8-overrides",
        ),
    ],
)
def test_torrent_filename_encoding(data: bytes, name: str, files: tuple[File, ...]) -> None:
    parser = TorrentParser(data=data)
    assert parser.name() == name
    assert parser.files() == files


def test_torrent_skips_directory_markers_but_keeps_empty_files() -> None:
    data = (
        b"d4:infod5:filesl"
        b"d6:lengthi0e4:pathl4:Subs0:ee"
        b"d6:lengthi0e4:pathl9:empty.binee"
        b"d6:lengthi7e4:pathl4:Subs11:English.assee"
        b"e4:name7:Releaseee"
    )
    parser = TorrentParser(data=data)
    assert parser.files() == (
        File("Release/empty.bin", size=0),
        File("Release/Subs/English.ass", size=7),
    )


def test_torrent_preserves_empty_file_list() -> None:
    data = b"d4:infod5:filesle4:name7:Releaseee"
    parser = TorrentParser(data=data)
    assert parser.files() == ()


@pytest.mark.parametrize("data", [b"d4:infodee", b"d4:infod4:name4:rootee"])
def test_torrent_requires_payload_layout(data: bytes) -> None:
    parser = TorrentParser(data=data)
    with pytest.raises(BencodeError, match="Torrent info must contain a name and either files or length"):
        parser.files()
