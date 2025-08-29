# type: ignore
from __future__ import annotations

from datetime import datetime

from torf import Torrent

from pynyaa import NyaaTorrentPage, Submitter, TorrentCategory


def test_submitter() -> None:
    a = Submitter(name="John", url="https://nyaa.si/user/john", is_trusted=True, is_banned=False)
    b = Submitter(name="John", url="https://nyaa.si/user/john", is_trusted=True, is_banned=False)
    c = Submitter(name="Jane", url="https://nyaa.si/user/jane", is_trusted=False, is_banned=False)
    assert a.__str__() == "John"

    assert a == b
    assert a != c
    assert c != "other"
    assert set((a, b, c)) == {a, c} == {b, c}


def test_nyaa_torrent_page() -> None:
    submitter_a = Submitter(name="John", url="https://nyaa.si/user/john", is_trusted=True, is_banned=False)
    page_a = NyaaTorrentPage(
        id=123456,
        url="https://nyaa.si/view/123456",
        title="title",
        category=TorrentCategory.ANIME_ENGLISH_TRANSLATED.value,
        submitter=submitter_a,
        datetime=datetime(year=2024, month=6, day=30),
        information=None,
        seeders=20,
        leechers=30,
        completed=100,
        is_trusted=False,
        is_remake=False,
        description=None,
        torrent_file="https://nyaa.si/download/123456.torrent",
        magnet="magnet:?xt=urn:btih:...&dn=...",
        torrent=Torrent.read(filepath="tests/__torrents__/ubuntu-22.04.4-live-server-amd64.iso.torrent"),
    )

    submitter_b = Submitter(name="John", url="https://nyaa.si/user/john", is_trusted=True, is_banned=False)
    page_b = NyaaTorrentPage(
        id=123456,
        url="https://nyaa.si/view/123456",
        title="title",
        category=TorrentCategory.ANIME_ENGLISH_TRANSLATED.value,
        submitter=submitter_b,
        datetime=datetime(year=2024, month=6, day=30),
        information=None,
        seeders=34,
        leechers=23,
        completed=123,
        is_trusted=True,
        is_remake=False,
        description="description",
        torrent_file="https://nyaa.si/download/123456.torrent",
        magnet="magnet:?xt=urn:btih:...&dn=...",
        torrent=Torrent.read(filepath="tests/__torrents__/ubuntu-22.04.4-live-server-amd64.iso.torrent"),
    )

    submitter_c = Submitter(name="Jane", url="https://nyaa.si/user/jane", is_trusted=False, is_banned=False)
    page_c = NyaaTorrentPage(
        id=567890,
        url="https://nyaa.si/view/567890",
        title="title",
        category=TorrentCategory.ANIME_ENGLISH_TRANSLATED.value,
        submitter=submitter_c,
        datetime=datetime(year=2024, month=6, day=30),
        information=None,
        seeders=34,
        leechers=23,
        completed=123,
        is_trusted=True,
        is_remake=False,
        description="description",
        torrent_file="https://nyaa.si/download/567890.torrent",
        magnet="magnet:?xt=urn:btih:...&dn=...",
        torrent=Torrent.read(filepath="tests/__torrents__/ubuntu-24.04-desktop-amd64.iso.torrent"),
    )

    assert str(page_a) == "title"

    assert page_a == page_b
    assert page_a != page_c
    assert page_c != "other"
    assert set((page_a, page_b, page_c)) == {page_a, page_c} == {page_b, page_c}
