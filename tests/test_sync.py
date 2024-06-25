from pynyaa import Nyaa, NyaaCategory, NyaaFilter

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}
client = Nyaa(headers=headers)


def test_nyaa_default() -> None:
    nyaa = client.get("https://nyaa.si/view/1755409")
    assert nyaa.title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"
    assert nyaa.submitter.name == "smol"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is False


def test_nyaa_trusted() -> None:
    description = """[I Want to Eat Your Pancreas](https://myanimelist.net/anime/36098/Kimi_no_Suizou_wo_Tabetai)

PAS subs, additional TS by [nedragrevev](https://github.com/nedragrevev/custom-subs).  
No 5.1 audio.

This BD had a lot of noise. I nuked the crap out of it. If you want a better encode with all the grain, grab a release that uses Beatrice-Raws (*not* D-Z0N3, that one is missing some scenes). For everyone else, this release looks much better than all the existing smaller and similar-sized encodes.

There is an alternate honorifics track in this release. Set your media player to play “enm” language tracks by default to automatically play honorifics tracks.

Please leave feedback in the comments, good or bad.  
Please read this short [playback guide](https://gist.github.com/motbob/754c24d5cd381334bb64b93581781a81) if you want to know how to make the video and subtitles of this release look better.
**Anyone wanting to do their own release is free to use any part of this torrent without permission or credit.**"""

    nyaa = client.get("https://nyaa.si/view/1544043")
    assert nyaa.title == "[MTBB] I Want to Eat Your Pancreas (BD 1080p) | Kimi no Suizou wo Tabetai"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.is_trusted is True
    assert nyaa.description == description
    assert nyaa.category == NyaaCategory.ANIME_ENGLISH_TRANSLATED


def test_nyaa_trusted_and_remake() -> None:
    nyaa = client.get("https://nyaa.si/view/1694824")
    assert (
        nyaa.title
        == "[MiniMTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
    )
    assert nyaa.is_remake is True
    assert nyaa.is_trusted is False
    assert nyaa.submitter.is_trusted is True


def test_nyaa_anon() -> None:
    nyaa = client.get(1765655)
    assert (
        nyaa.title
        == "[Kinoworm] Ascendance of a Bookworm P01v01-P05v08 + Fanbook v01-v03 + Royal Academy Stories First Year v01 + Short Story Collection v01 (J-Novel Club) (Premium)"
    )
    assert nyaa.url.__str__() == "https://nyaa.si/view/1765655"
    assert nyaa.information == "https://www.goodreads.com/series/220639-ascendance-of-a-bookworm-light-novel"
    assert nyaa.submitter.name == "Anonymous"
    assert nyaa.category == NyaaCategory.LITERATURE_ENGLISH_TRANSLATED


def test_nyaa_banned() -> None:
    nyaa = client.get("https://nyaa.si/view/1422797")
    assert nyaa.title == "[succ_] Tsugumomo [BDRip 1920x1080 x264 FLAC]"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 20


def test_nyaa_banned_and_trusted() -> None:
    nyaa = client.get("https://nyaa.si/view/884488")
    assert nyaa.title == "[FMA1394] Fullmetal Alchemist (2003) [Dual Audio] [US BD] (batch)"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 51


def test_nyaa_empty_desc_info() -> None:
    nyaa = client.get("https://nyaa.si/view/1586776")
    assert nyaa.information is None
    assert nyaa.description is None


def test_nyaa_search() -> None:
    zero = client.search("akldlaskdjsaljdksd")
    assert zero == tuple()

    single = client.search("smol shelter")
    assert single[0].title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"

    single = client.search('"[smol] Shelter (2016) (BD 1080p HEVC FLAC)"', limit=74)
    assert single[0].title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"

    limited = client.search("smol", limit=2)
    assert len(limited) == 2

    limited_not_trusted_literature = client.search("smol", category=NyaaCategory.LITERATURE_ENGLISH_TRANSLATED, filter=NyaaFilter.TRUSTED_ONLY, limit=2)
    assert len(limited_not_trusted_literature) == 0

    limited_trusted_english = client.search("mtbb", category=NyaaCategory.ANIME_ENGLISH_TRANSLATED, filter=NyaaFilter.NO_FILTER, limit=2)
    assert len(limited_trusted_english) == 2
