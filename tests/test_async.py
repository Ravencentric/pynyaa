# type: ignore
from pynyaa import AsyncNyaa, NyaaCategory, NyaaFilter

from .helpers import get_response, get_search, get_torrent

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
client = AsyncNyaa(headers=headers)

async def test_nyaa_default(respx_mock) -> None:
    respx_mock.get("https://nyaa.si/view/1755409").mock(return_value=get_response(1755409))
    respx_mock.get("https://nyaa.si/download/1755409.torrent").mock(return_value=get_torrent(1755409))

    nyaa = await client.get("https://nyaa.si/view/1755409")
    assert nyaa.title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"
    assert nyaa.submitter.name == "smol"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is False


async def test_nyaa_trusted(respx_mock) -> None:
    description = """[I Want to Eat Your Pancreas](https://myanimelist.net/anime/36098/Kimi_no_Suizou_wo_Tabetai)

PAS subs, additional TS by [nedragrevev](https://github.com/nedragrevev/custom-subs).  
No 5.1 audio.

This BD had a lot of noise. I nuked the crap out of it. If you want a better encode with all the grain, grab a release that uses Beatrice-Raws (*not* D-Z0N3, that one is missing some scenes). For everyone else, this release looks much better than all the existing smaller and similar-sized encodes.

There is an alternate honorifics track in this release. Set your media player to play “enm” language tracks by default to automatically play honorifics tracks.

Please leave feedback in the comments, good or bad.  
Please read this short [playback guide](https://gist.github.com/motbob/754c24d5cd381334bb64b93581781a81) if you want to know how to make the video and subtitles of this release look better.
**Anyone wanting to do their own release is free to use any part of this torrent without permission or credit.**"""

    respx_mock.get("https://nyaa.si/view/1544043").mock(return_value=get_response(1544043))
    respx_mock.get("https://nyaa.si/download/1544043.torrent").mock(return_value=get_torrent(1544043))

    nyaa = await client.get("https://nyaa.si/view/1544043")
    assert nyaa.title == "[MTBB] I Want to Eat Your Pancreas (BD 1080p) | Kimi no Suizou wo Tabetai"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.is_trusted is True
    assert nyaa.description == description
    assert nyaa.category == NyaaCategory.ANIME_ENGLISH_TRANSLATED


async def test_nyaa_trusted_and_remake(respx_mock) -> None:
    respx_mock.get("https://nyaa.si/view/1694824").mock(return_value=get_response(1694824))
    respx_mock.get("https://nyaa.si/download/1694824.torrent").mock(return_value=get_torrent(1694824))

    nyaa = await client.get("https://nyaa.si/view/1694824")
    assert (
        nyaa.title
        == "[MiniMTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
    )
    assert nyaa.is_remake is True
    assert nyaa.is_trusted is False
    assert nyaa.submitter.is_trusted is True


async def test_nyaa_anon(respx_mock) -> None:
    respx_mock.get("https://nyaa.si/view/1765655").mock(return_value=get_response(1765655))
    respx_mock.get("https://nyaa.si/download/1765655.torrent").mock(return_value=get_torrent(1765655))

    nyaa = await client.get(1765655)
    assert (
        nyaa.title
        == "[Kinoworm] Ascendance of a Bookworm P01v01-P05v08 + Fanbook v01-v03 + Royal Academy Stories First Year v01 + Short Story Collection v01 (J-Novel Club) (Premium)"
    )
    assert nyaa.url.__str__() == "https://nyaa.si/view/1765655"
    assert nyaa.information == "https://www.goodreads.com/series/220639-ascendance-of-a-bookworm-light-novel"
    assert nyaa.submitter.name == "Anonymous"
    assert nyaa.category == NyaaCategory.LITERATURE_ENGLISH_TRANSLATED


async def test_nyaa_banned(respx_mock) -> None:
    # Thoughts and Prayers for our good friend succ_
    respx_mock.get("https://nyaa.si/view/1422797").mock(return_value=get_response(1422797))
    respx_mock.get("https://nyaa.si/download/1422797.torrent").mock(return_value=get_torrent(1422797))

    nyaa = await client.get("https://nyaa.si/view/1422797")
    assert nyaa.title == "[succ_] Tsugumomo [BDRip 1920x1080 x264 FLAC]"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 20


async def test_nyaa_banned_and_trusted(respx_mock) -> None:
    respx_mock.get("https://nyaa.si/view/884488").mock(return_value=get_response(884488))
    respx_mock.get("https://nyaa.si/download/884488.torrent").mock(return_value=get_torrent(884488))

    nyaa = await client.get("https://nyaa.si/view/884488")
    assert nyaa.title == "[FMA1394] Fullmetal Alchemist (2003) [Dual Audio] [US BD] (batch)"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 51


async def test_nyaa_empty_desc_info(respx_mock) -> None:
    respx_mock.get("https://nyaa.si/view/1586776").mock(return_value=get_response(1586776))
    respx_mock.get("https://nyaa.si/download/1586776.torrent").mock(return_value=get_torrent(1586776))

    nyaa = await client.get("https://nyaa.si/view/1586776")
    assert nyaa.information is None
    assert nyaa.description is None


async def test_nyaa_search_empty(respx_mock) -> None:
    respx_mock.get("https://nyaa.si?page=rss&f=0&c=0_0&q=akldlaskdjsaljdksd").mock(
        return_value=get_search("akldlaskdjsaljdksd")
    )

    zero = await client.search("akldlaskdjsaljdksd")
    assert zero == tuple()


async def test_search_single(respx_mock) -> None:
    respx_mock.get("https://nyaa.si?page=rss&f=0&c=0_0&q=smol%20shelter").mock(return_value=get_search("smol shelter"))
    respx_mock.get("https://nyaa.si/view/1755409").mock(return_value=get_response(1755409))
    respx_mock.get("https://nyaa.si/download/1755409.torrent").mock(return_value=get_torrent(1755409))

    single = await client.search("smol shelter")
    assert single[0].title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"

    single_with_limit = await client.search('"[smol] Shelter (2016) (BD 1080p HEVC FLAC)"', limit=74)
    assert single_with_limit[0].title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"


async def test_search_0_results(respx_mock) -> None:
    respx_mock.get("https://nyaa.si?page=rss&f=2&c=3_1&q=vodes").mock(return_value=get_search("vodes"))
    limited_not_trusted_literature = await client.search(
        "vodes", category=NyaaCategory.LITERATURE_ENGLISH_TRANSLATED, filter=NyaaFilter.TRUSTED_ONLY, limit=2
    )
    assert len(limited_not_trusted_literature) == 0


async def test_search_filtered(respx_mock) -> None:
    respx_mock.get("https://nyaa.si?page=rss&f=0&c=1_2&q=mtbb").mock(return_value=get_search("mtbb"))

    respx_mock.get("https://nyaa.si/view/1837736").mock(return_value=get_response(1837736))
    respx_mock.get("https://nyaa.si/download/1837736.torrent").mock(return_value=get_torrent(1837736))

    respx_mock.get("https://nyaa.si/view/1837420").mock(return_value=get_response(1837420))
    respx_mock.get("https://nyaa.si/download/1837420.torrent").mock(return_value=get_torrent(1837420))

    limited_trusted_english = await client.search(
        "mtbb", category=NyaaCategory.ANIME_ENGLISH_TRANSLATED, filter=NyaaFilter.NO_FILTER, limit=2
    )
    assert len(limited_trusted_english) == 2
