from pynyaa import AsyncNyaa, NyaaCategory

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
client = AsyncNyaa(headers=headers)


async def test_nyaa_default() -> None:
    nyaa = await client.get("https://nyaa.si/view/1755409")
    assert nyaa.title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"
    assert nyaa.submitter.name == "smol"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is False


async def test_nyaa_trusted() -> None:
    description = """[I Want to Eat Your Pancreas](https://myanimelist.net/anime/36098/Kimi_no_Suizou_wo_Tabetai)

PAS subs, additional TS by [nedragrevev](https://github.com/nedragrevev/custom-subs).  
No 5.1 audio.

This BD had a lot of noise. I nuked the crap out of it. If you want a better encode with all the grain, grab a release that uses Beatrice-Raws (*not* D-Z0N3, that one is missing some scenes). For everyone else, this release looks much better than all the existing smaller and similar-sized encodes.

There is an alternate honorifics track in this release. Set your media player to play “enm” language tracks by default to automatically play honorifics tracks.

Please leave feedback in the comments, good or bad.  
Please read this short [playback guide](https://gist.github.com/motbob/754c24d5cd381334bb64b93581781a81) if you want to know how to make the video and subtitles of this release look better.
**Anyone wanting to do their own release is free to use any part of this torrent without permission or credit.**"""

    nyaa = await client.get("https://nyaa.si/view/1544043")
    assert nyaa.title == "[MTBB] I Want to Eat Your Pancreas (BD 1080p) | Kimi no Suizou wo Tabetai"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.is_trusted is True
    assert nyaa.description == description
    assert nyaa.category == NyaaCategory.ANIME_ENGLISH_TRANSLATED


async def test_nyaa_trusted_and_remake() -> None:
    nyaa = await client.get("https://nyaa.si/view/1694824")
    assert (
        nyaa.title
        == "[MiniMTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
    )
    assert nyaa.is_remake is True
    assert nyaa.is_trusted is False
    assert nyaa.submitter.is_trusted is True


async def test_nyaa_anon() -> None:
    nyaa = await client.get(1765655)
    assert (
        nyaa.title
        == "[Kinoworm] Ascendance of a Bookworm P01v01-P05v08 + Fanbook v01-v03 + Royal Academy Stories First Year v01 + Short Story Collection v01 (J-Novel Club) (Premium)"
    )
    assert nyaa.url.__str__() == "https://nyaa.si/view/1765655"
    assert nyaa.information == "https://www.goodreads.com/series/220639-ascendance-of-a-bookworm-light-novel"
    assert nyaa.submitter.name == "Anonymous"
    assert nyaa.category == NyaaCategory.LITERATURE_ENGLISH_TRANSLATED


async def test_nyaa_banned_and_trusted() -> None:
    nyaa = await client.get("https://nyaa.si/view/884488")
    assert nyaa.title == "[FMA1394] Fullmetal Alchemist (2003) [Dual Audio] [US BD] (batch)"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 51


async def test_nyaa_empty_desc_info() -> None:
    nyaa = await client.get("https://nyaa.si/view/1586776")
    assert nyaa.information == "No information."
    assert nyaa.description == "#### No description."
