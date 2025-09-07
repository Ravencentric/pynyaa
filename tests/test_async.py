from __future__ import annotations

import datetime as dt
import textwrap

import pytest

from pynyaa import AsyncNyaa, Category, Filter, Order, Submitter


def dedent(s: str) -> str:
    return textwrap.dedent(s).strip()


async def test_properties(async_nyaa_client: AsyncNyaa) -> None:
    assert async_nyaa_client.base_url == "https://nyaa.si/"


@pytest.mark.vcr
async def test_nyaa_default(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1755409")
    assert nyaa.id == 1755409
    assert nyaa.url == "https://nyaa.si/view/1755409"
    assert nyaa.title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"
    assert nyaa.category is Category.ANIME_ENGLISH_TRANSLATED
    assert nyaa.submitter == Submitter(
        name="smol",
        url="https://nyaa.si/user/smol",
        is_trusted=False,
        is_banned=False,
    )
    assert nyaa.datetime == dt.datetime(2023, 12, 14, 9, 6, 18, tzinfo=dt.timezone.utc)
    assert nyaa.information == "https://anidb.net/anime/12482"
    assert nyaa.seeders == 15
    assert nyaa.leechers == 0
    assert nyaa.completed == 640
    assert nyaa.is_trusted is False
    assert nyaa.is_remake is False
    assert nyaa.description == dedent("""
    Video: JPBD (Sony). Encoded by smolkitten.
    Audio: Japanese FLAC (2.0)
    Subtitles: Full subtitles [Harunatsu]
    [Mediainfo](https://pastebin.com/tLu6yxTZ) | [Comparisons](https://slow.pics/c/oPk6POK1) | [Discord](https://discord.gg/5QknG2PP6D)

    Harunatsu's subtitles were restyled.
    """)
    assert nyaa.size == 619603559
    assert nyaa.infohash == "ad596c24e64424aa6fe02c04c20eb25e57dbb042"
    assert nyaa.torrent == "https://nyaa.si/download/1755409.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:ad596c24e64424aa6fe02c04c20eb25e57dbb042")


@pytest.mark.vcr
async def test_nyaa_trusted(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1544043")
    assert nyaa.id == 1544043
    assert nyaa.url == "https://nyaa.si/view/1544043"
    assert nyaa.title == "[MTBB] I Want to Eat Your Pancreas (BD 1080p) | Kimi no Suizou wo Tabetai"
    assert nyaa.category is Category.ANIME_ENGLISH_TRANSLATED
    assert nyaa.submitter == Submitter(
        name="motbob",
        url="https://nyaa.si/user/motbob",
        is_trusted=True,
        is_banned=False,
    )
    assert nyaa.datetime == dt.datetime(2022, 6, 20, 0, 0, 18, tzinfo=dt.timezone.utc)
    assert nyaa.information == "#MTBB on Rizon"
    assert nyaa.seeders == 30
    assert nyaa.leechers == 0
    assert nyaa.completed == 3895
    assert nyaa.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.description == dedent("""
    [I Want to Eat Your Pancreas](https://myanimelist.net/anime/36098/Kimi_no_Suizou_wo_Tabetai)

    PAS subs, additional TS by [nedragrevev](https://github.com/nedragrevev/custom-subs).  
    No 5.1 audio.

    This BD had a lot of noise. I nuked the crap out of it. If you want a better encode with all the grain, grab a release that uses Beatrice-Raws (*not* D-Z0N3, that one is missing some scenes). For everyone else, this release looks much better than all the existing smaller and similar-sized encodes.

    There is an alternate honorifics track in this release. Set your media player to play “enm” language tracks by default to automatically play honorifics tracks.

    Please leave feedback in the comments, good or bad.  
    Please read this short [playback guide](https://gist.github.com/motbob/754c24d5cd381334bb64b93581781a81) if you want to know how to make the video and subtitles of this release look better.
    All components of this release are released into the public domain to the [greatest extent possible](https://gist.github.com/motbob/9a85edadca33c7b8a3bb4de23396d510).
    """)
    assert nyaa.size == 2040109466
    assert nyaa.infohash == "78e51b8285dd611dc1728d9b38dc1b8607cd0994"
    assert nyaa.torrent == "https://nyaa.si/download/1544043.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:78e51b8285dd611dc1728d9b38dc1b8607cd0994")


@pytest.mark.vcr
async def test_nyaa_trusted_and_remake(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1694824")
    assert nyaa.id == 1694824
    assert nyaa.url == "https://nyaa.si/view/1694824"
    assert nyaa.title == dedent("""
    [MiniMTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale
    """)
    assert nyaa.category is Category.ANIME_ENGLISH_TRANSLATED
    assert nyaa.submitter == Submitter(
        name="motbob",
        url="https://nyaa.si/user/motbob",
        is_trusted=True,
        is_banned=False,
    )
    assert nyaa.datetime == dt.datetime(2023, 7, 19, 15, 18, 2, tzinfo=dt.timezone.utc)
    assert nyaa.information == "https://discord.gg/r9gyPwJeqW"
    assert nyaa.seeders == 10
    assert nyaa.leechers == 0
    assert nyaa.completed == 982
    assert nyaa.is_trusted is False
    assert nyaa.is_remake is True
    assert nyaa.description == dedent("""
    This is a smaller and lower quality version of [Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p)](https://nyaa.si/view/1694821).

    Since these videos are 10-bit AV1, you should make sure you have a fully updated version of your video player to avoid playback issues, whether it's [MPC](https://github.com/clsid2/mpc-hc/releases/tag/2.0.0), [mpv](https://mpv.io/), or [VLC](https://www.videolan.org/vlc/).
    """)
    assert nyaa.size == 1288490189
    assert nyaa.infohash == "19606f2e09b7013d9fcefbb67955766c19c32c5a"
    assert nyaa.torrent == "https://nyaa.si/download/1694824.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:19606f2e09b7013d9fcefbb67955766c19c32c5a")


@pytest.mark.vcr
async def test_nyaa_anon(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get(1765655)

    assert nyaa.id == 1765655
    assert nyaa.url == "https://nyaa.si/view/1765655"
    assert nyaa.title == dedent("""
    [Kinoworm] Ascendance of a Bookworm P01v01-P05v08 + Fanbook v01-v03 + Royal Academy Stories First Year v01 + Short Story Collection v01 (J-Novel Club) (Premium)    
    """)
    assert nyaa.category is Category.LITERATURE_ENGLISH_TRANSLATED
    assert nyaa.submitter is None
    assert nyaa.datetime == dt.datetime(2024, 1, 13, 7, 20, 33, tzinfo=dt.timezone.utc)
    assert nyaa.information == "https://www.goodreads.com/series/220639-ascendance-of-a-bookworm-light-novel"
    assert nyaa.seeders == 6
    assert nyaa.leechers == 0
    assert nyaa.completed == 707
    assert nyaa.is_trusted is False
    assert nyaa.is_remake is False
    assert nyaa.description == dedent("""
    ### Join [![](https://discordapp.com/api/guilds/974468300304171038/widget.png?style=banner2)](https://discord.gg/snackbox) for bookworm cult
    ---

    ![](https://files.catbox.moe/7dr7oc.png)

    Sorry about that, my house got raided because my drug dealer snitched on me.

    ---

    ### Update
    - Added P5v08 Premium from AnimationBytings

    ---

    ### Bonus
    Final volume of the Kinoworm saga

    ![](https://files.catbox.moe/8bfabf.png)

    ---

    ### How to read this? 
    Go here https://thewiki.moe/getting-started/literature
    """)
    assert nyaa.size == 1288490189
    assert nyaa.infohash == "8732a06d2087c71fddf5dc55d08512ebe146d445"
    assert nyaa.torrent == "https://nyaa.si/download/1765655.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:8732a06d2087c71fddf5dc55d08512ebe146d445")


@pytest.mark.vcr
async def test_nyaa_banned(async_nyaa_client: AsyncNyaa) -> None:
    # Thoughts and Prayers for our good friend succ_
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1422797")
    assert nyaa.id == 1422797
    assert nyaa.url == "https://nyaa.si/view/1422797"
    assert nyaa.title == "[succ_] Tsugumomo [BDRip 1920x1080 x264 FLAC]"
    assert nyaa.category is Category.ANIME_ENGLISH_TRANSLATED
    assert nyaa.submitter == Submitter(
        name="darkmodejesus",
        url="https://nyaa.si/user/darkmodejesus",
        is_trusted=False,
        is_banned=True,
    )
    assert nyaa.datetime == dt.datetime(2021, 8, 19, 14, 56, 35, tzinfo=dt.timezone.utc)
    assert nyaa.information == "@succ_#2864 on discord"
    assert nyaa.seeders == 3
    assert nyaa.leechers == 1
    assert nyaa.completed == 117
    assert nyaa.is_trusted is False
    assert nyaa.is_remake is False
    assert nyaa.description == dedent("""
    #### This is not a meme release
    | Sources |            |
    | ------------- |:-------------:|
    | Video      | [Beatrice-Raws](https://nyaa.si/view/1015456) (AVC) |
    | Audio      | [Beatrice-Raws](https://nyaa.si/view/1015456) (Japanese 2.0 FLAC 24-bit) |
    | Subs | Astral|
    | Extras| [Beatrice-Raws](https://nyaa.si/view/1015456) (NC and BD Menus)|
    **mods pls don't ban me I deleted the last torrent bc I had a config issue and had to create a new one**

    **Notes:**
    -Slapped Astral's subs on Beatrice's video, that's it, there's no meme.
    -This is my first time doing a mux of a series so errors might have gone unnoticed, feel free to comment any of your insatisfactions with this release here or if the problem is serious message me on discord.
    -No subs added to the NCs cuz I'm afraid to fuck something up.

    For playback I recommend mpv (if the lack of UI bother you get [mpv.net](https://github.com/stax76/mpv.net)) or MPC-BE

    ### Enjoy and seed for as long as you can!
    [Ep 01 Mediainfo](https://pastebin.com/GdANdZnz)
    ![alt text](https://files.catbox.moe/wwat45.png "booba")

    ### Torrent died cba to reseed, get it from [animetosho](https://animetosho.org/view/succ_-tsugumomo-bdrip-1920x1080-x264-flac.n1422797) or [mega](https://mega.nz/folder/dlhEFBCR#QWJMFi2chNH8TIwHwU6UJg)
    """)
    assert nyaa.size == 18360985191
    assert nyaa.infohash == "5fecba4e64910a38c05d7566131a1318133bbc45"
    assert nyaa.torrent == "https://nyaa.si/download/1422797.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:5fecba4e64910a38c05d7566131a1318133bbc45")


@pytest.mark.vcr
async def test_nyaa_banned_and_trusted(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/884488")
    assert nyaa.id == 884488
    assert nyaa.url == "https://nyaa.si/view/884488"
    assert nyaa.title == "[FMA1394] Fullmetal Alchemist (2003) [Dual Audio] [US BD] (batch)"
    assert nyaa.category is Category.ANIME_ENGLISH_TRANSLATED
    assert nyaa.submitter == Submitter(
        name="FMA1394",
        url="https://nyaa.si/user/FMA1394",
        is_trusted=True,
        is_banned=True,
    )
    assert nyaa.datetime == dt.datetime(2016, 12, 27, 1, 13, tzinfo=dt.timezone.utc)
    assert nyaa.information is None
    assert nyaa.seeders == 16
    assert nyaa.leechers == 3
    assert nyaa.completed == 5915
    assert nyaa.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.description
    assert nyaa.size == 20293720474
    assert nyaa.infohash == "2959e97cb7796f029d2196fb63bb5c70b56d4206"
    assert nyaa.torrent == "https://nyaa.si/download/884488.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:2959e97cb7796f029d2196fb63bb5c70b56d4206")


@pytest.mark.vcr
async def test_nyaa_description(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1992716")
    assert nyaa.id == 1992716
    assert nyaa.url == "https://nyaa.si/view/1992716"
    assert nyaa.title == "[MTBB] Steins;Gate 0 (BD 1080p) | Steins;Gate Zero S1"
    assert nyaa.category is Category.ANIME_ENGLISH_TRANSLATED
    assert nyaa.submitter == Submitter(
        name="motbob",
        url="https://nyaa.si/user/motbob",
        is_trusted=True,
        is_banned=False,
    )
    assert nyaa.datetime == dt.datetime(2025, 7, 13, 9, 51, 18, tzinfo=dt.timezone.utc)
    assert nyaa.information == "https://discord.gg/r9gyPwJeqW"
    assert nyaa.seeders == 104
    assert nyaa.leechers == 6
    assert nyaa.completed == 1112
    assert nyaa.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.description == dedent("""
    [Steins;Gate 0](https://myanimelist.net/anime/30484/Steins_Gate_0)

    **Original subs**: WhyNot (23β), LostYears (01-23), GhostYears (24)  
    **TLC (dialogue)**: GeeYu (01-23)  
    **QC/editing**: motbob  
    **Additional QC**: arsenyshalin  

    You should probably watch "Episode 23β" (S00E01 in the Specials folder) before anything else. You should also read up on [Tanabata](https://en.wikipedia.org/wiki/Tanabata) if you're unfamiliar with its lore. Note that I omitted "probably" in that last sentence. Go do it.

    There are alternate honorifics tracks in this release. Set your media player to play "enm" language tracks by default to automatically play honorifics tracks.

    [Video quality comparisons](https://slow.pics/c/QtLFD8uA)  

    Please leave feedback in the comments, good or bad.  
    Please read this short [playback guide](https://gist.github.com/motbob/754c24d5cd381334bb64b93581781a81) if you want to know how to make the video and subtitles of this release look better.
    All components of this release are released into the public domain to the [greatest extent possible](https://gist.github.com/motbob/9a85edadca33c7b8a3bb4de23396d510).    
    """)
    assert nyaa.size == 44667659879
    assert nyaa.infohash == "489cb384b126a87e26afc0dfe96ef20216a2fc39"
    assert nyaa.torrent == "https://nyaa.si/download/1992716.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:489cb384b126a87e26afc0dfe96ef20216a2fc39")


@pytest.mark.vcr
async def test_nyaa_empty_info(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/5819")
    assert nyaa.id == 5819
    assert nyaa.url == "https://nyaa.si/view/5819"
    assert nyaa.title == "[moyism] Myself;Yourself - 08 (RAW)"
    assert nyaa.category is Category.ANIME_RAW
    assert nyaa.submitter == Submitter(
        name="NyaaTorrents", url="https://nyaa.si/user/NyaaTorrents", is_trusted=False, is_banned=False
    )
    assert nyaa.datetime == dt.datetime(2008, 6, 23, 3, 24, tzinfo=dt.timezone.utc)
    assert nyaa.information is None
    assert nyaa.seeders == 0
    assert nyaa.leechers == 0
    assert nyaa.completed == 0
    assert nyaa.is_trusted is False
    assert nyaa.is_remake is False
    assert nyaa.description == "Share - YS2YSUOe1cLtf - D-tvk DivX6.6 704x396"
    assert nyaa.size == 192728269
    assert nyaa.infohash == "ad35645d31cf4110440a79b062f775bcab717af3"
    assert nyaa.torrent == "https://nyaa.si/download/5819.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:ad35645d31cf4110440a79b062f775bcab717af3")


@pytest.mark.vcr
async def test_nyaa_empty_desc(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/76777")
    assert nyaa.id == 76777
    assert nyaa.url == "https://nyaa.si/view/76777"
    assert nyaa.title == "[CommieRaws]GA Geijutsuka Art Design Class 03 848x480[13BADBC6].mkv"
    assert nyaa.category is Category.ANIME_RAW
    assert nyaa.submitter == Submitter(
        name="NyaaTorrents", url="https://nyaa.si/user/NyaaTorrents", is_trusted=False, is_banned=False
    )
    assert nyaa.datetime == dt.datetime(2009, 7, 24, 23, 47, tzinfo=dt.timezone.utc)
    assert nyaa.information == "irc://irc.rizon.net/commie"
    assert nyaa.seeders == 0
    assert nyaa.leechers == 0
    assert nyaa.completed == 0
    assert nyaa.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.description is None
    assert nyaa.size == 178887066
    assert nyaa.infohash == "88cbf145c04d79e103a4620543098848544283ad"
    assert nyaa.torrent == "https://nyaa.si/download/76777.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:88cbf145c04d79e103a4620543098848544283ad")


@pytest.mark.vcr
async def test_nyaa_empty_desc_info(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1586776")
    assert nyaa.id == 1586776
    assert nyaa.url == "https://nyaa.si/view/1586776"
    assert nyaa.title == "Hatsune Miku - Angel Call -Vocaloid-PV clips Blu-ray Edition- [kuchikirukia]"
    assert nyaa.category is Category.ANIME_MUSIC_VIDEO
    assert nyaa.submitter == Submitter(
        name="kuchikirukia", url="https://nyaa.si/user/kuchikirukia", is_trusted=False, is_banned=False
    )
    assert nyaa.datetime == dt.datetime(2022, 10, 5, 20, 35, 18, tzinfo=dt.timezone.utc)
    assert nyaa.information is None
    assert nyaa.seeders == 2
    assert nyaa.leechers == 0
    assert nyaa.completed == 127
    assert nyaa.is_trusted is False
    assert nyaa.is_remake is False
    assert nyaa.description is None
    assert nyaa.size == 2576980378
    assert nyaa.infohash == "79f9947ec567f1d5edb6ea472818588881094b2f"
    assert nyaa.torrent == "https://nyaa.si/download/1586776.torrent"
    assert nyaa.magnet.startswith("magnet:?xt=urn:btih:79f9947ec567f1d5edb6ea472818588881094b2f")


@pytest.mark.vcr
async def test_search(async_nyaa_client: AsyncNyaa) -> None:
    results = async_nyaa_client.search("MTBB", order=Order.ASCENDING)
    titles = [torrent.title async for torrent in results]
    assert len(titles) > 150
    assert titles[:10] == [
        "[MTBB] Psycho-Pass: The Movie: Engrish Eradication Edition (BD 1080p)",
        "[MTBB] Your Name. (1080p BD) | Kimi no Na wa.",
        "[MTBB] Mobile Suit Gundam 0080: War in the Pocket (720p BD)",
        "[MTBB] Classroom of the Elite S1 (WEB 720p) | Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e",
        "[MTBB] Yahari Ore no Seishun Love Comedy wa Machigatteiru. Zoku - OVA (720p BD)",
        "[MTBB] In This Corner of the World (1080p BD) | Kono Sekai no Katasumi ni",
        "[MTBB] Inuyashiki (WEB 810p)",
        "[MTBB] Mind Game (810p BD)",
        "[MTBB] One Stormy Night (WEB 1080p) | Arashi no Yoru ni",
        "[MTBB] Hakumei to Mikochi - OVA (BD 720p)",
    ]  # Page 1
    assert "[MTBB] Hyouka (BD 1080p)" in titles  # Page 2
    assert "[MTBB] Katanagatari S1 (BD 1080p)" in titles  # Page 3

    assert "[MTBB] Sword Art Online - Alicization (Unofficial Batch)" in titles  # Uploaded by someone else
    assert (
        "[MTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
        in titles  # Uploaded by MTBB but not marked Trusted
    )
    assert "[MTBB-Minis] Monogatari Series (BD 1080p AV1)" in titles  # REMAKE


@pytest.mark.vcr
async def test_search_trusted_only(async_nyaa_client: AsyncNyaa) -> None:
    results = async_nyaa_client.search("MTBB", filter=Filter.TRUSTED_ONLY, order=Order.ASCENDING)
    titles = [torrent.title async for torrent in results]
    assert titles[:10] == [
        "[MTBB] Psycho-Pass: The Movie: Engrish Eradication Edition (BD 1080p)",
        "[MTBB] Your Name. (1080p BD) | Kimi no Na wa.",
        "[MTBB] Mobile Suit Gundam 0080: War in the Pocket (720p BD)",
        "[MTBB] Classroom of the Elite S1 (WEB 720p) | Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e",
        "[MTBB] Yahari Ore no Seishun Love Comedy wa Machigatteiru. Zoku - OVA (720p BD)",
        "[MTBB] In This Corner of the World (1080p BD) | Kono Sekai no Katasumi ni",
        "[MTBB] Inuyashiki (WEB 810p)",
        "[MTBB] Mind Game (810p BD)",
        "[MTBB] One Stormy Night (WEB 1080p) | Arashi no Yoru ni",
        "[MTBB] Hakumei to Mikochi - OVA (BD 720p)",
    ]  # Page 1
    assert "[MTBB] Hyouka (BD 1080p)" in titles  # Page 2
    assert "[MTBB] Katanagatari S1 (BD 1080p)" in titles  # Page 3

    assert "[MTBB] Sword Art Online - Alicization (Unofficial Batch)" not in titles  # Uploaded by someone else
    assert (
        "[MTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
        not in titles  # Uploaded by MTBB but not marked Trusted
    )
    assert "[MTBB-Minis] Monogatari Series (BD 1080p AV1)" in titles  # REMAKE


@pytest.mark.vcr
async def test_search_no_remakes(async_nyaa_client: AsyncNyaa) -> None:
    results = async_nyaa_client.search("MTBB", filter=Filter.NO_REMAKES, order=Order.ASCENDING)
    titles = [torrent.title async for torrent in results]
    assert titles[:10] == [
        "[MTBB] Psycho-Pass: The Movie: Engrish Eradication Edition (BD 1080p)",
        "[MTBB] Your Name. (1080p BD) | Kimi no Na wa.",
        "[MTBB] Mobile Suit Gundam 0080: War in the Pocket (720p BD)",
        "[MTBB] Classroom of the Elite S1 (WEB 720p) | Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e",
        "[MTBB] Yahari Ore no Seishun Love Comedy wa Machigatteiru. Zoku - OVA (720p BD)",
        "[MTBB] In This Corner of the World (1080p BD) | Kono Sekai no Katasumi ni",
        "[MTBB] Inuyashiki (WEB 810p)",
        "[MTBB] Mind Game (810p BD)",
        "[MTBB] One Stormy Night (WEB 1080p) | Arashi no Yoru ni",
        "[MTBB] Hakumei to Mikochi - OVA (BD 720p)",
    ]  # Page 1
    assert "[MTBB] Hyouka (BD 1080p)" in titles  # Page 2
    assert "[MTBB] Katanagatari S1 (BD 1080p)" in titles  # Page 3

    assert "[MTBB] Sword Art Online - Alicization (Unofficial Batch)" in titles  # Uploaded by someone else
    assert (
        "[MTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
        in titles  # Uploaded by MTBB but not marked Trusted
    )
    assert "[MTBB-Minis] Monogatari Series (BD 1080p AV1)" not in titles  # REMAKE


@pytest.mark.vcr
async def test_nyaa_search_no_results(async_nyaa_client: AsyncNyaa) -> None:
    results = async_nyaa_client.search("akldlaskdjsaljdksd")  # 0 results
    assert [i async for i in results] == []
