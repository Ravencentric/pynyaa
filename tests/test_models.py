# type: ignore
from datetime import datetime

from pynyaa import NyaaCategory, NyaaTorrentPage, Submitter
from torf import Torrent


def test_submitter() -> None:
    a = Submitter(name="John", url="https://nyaa.si/user/john", is_trusted=True, is_banned=False)
    b = Submitter(name="John", url="https://nyaa.si/user/john", is_trusted=True, is_banned=False)
    c = Submitter(name="Jane", url="https://nyaa.si/user/jane", is_trusted=False, is_banned=False)

    assert a.__repr__() == "Submitter(name='John', url='https://nyaa.si/user/john', is_trusted=True, is_banned=False)"
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
        category=NyaaCategory.ANIME_ENGLISH_TRANSLATED.value,
        submitter=submitter_a,
        date=datetime(year=2024, month=6, day=30),
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
        category=NyaaCategory.ANIME_ENGLISH_TRANSLATED.value,
        submitter=submitter_b,
        date=datetime(year=2024, month=6, day=30),
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
        category=NyaaCategory.ANIME_ENGLISH_TRANSLATED.value,
        submitter=submitter_c,
        date=datetime(year=2024, month=6, day=30),
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

    assert (
        page_a.__repr__()
        == "NyaaTorrentPage(title='title', url='https://nyaa.si/view/123456', category='Anime - English-translated', date='2024-06-30T00:00:00', submitter='John')"
    )
    assert page_a.__str__() == "title"

    assert page_a == page_b
    assert page_a != page_c
    assert page_c != "other"
    assert set((page_a, page_b, page_c)) == {page_a, page_c} == {page_b, page_c}

    assert (
        page_a.model_dump_json()
        == """{"id":123456,"url":"https://nyaa.si/view/123456","title":"title","category":"Anime - English-translated","date":"2024-06-30T00:00:00","submitter":{"name":"John","url":"https://nyaa.si/user/john","is_trusted":true,"is_banned":false},"information":null,"seeders":20,"leechers":30,"completed":100,"is_trusted":false,"is_remake":false,"description":null,"torrent_file":"https://nyaa.si/download/123456.torrent","magnet":"magnet:?xt=urn:btih:...&dn=...","torrent":{"name":"ubuntu-22.04.4-live-server-amd64.iso","size":2104408064,"infohash":"4d29c6c02c97caad937d8a9b66b0bb1b6f7cbbfe","piece_size":262144,"private":null,"trackers":[["https://torrent.ubuntu.com/announce"],["https://ipv6.torrent.ubuntu.com/announce"]],"comment":"Ubuntu CD releases.ubuntu.com","creation_date":null,"created_by":"mktorrent 1.1","source":null,"files":[{"file":"ubuntu-22.04.4-live-server-amd64.iso","size":2104408064}]}}"""
    )
