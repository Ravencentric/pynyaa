from __future__ import annotations

from pynyaa import AsyncNyaa, Category


async def test_properties(async_nyaa_client: AsyncNyaa) -> None:
    assert async_nyaa_client.base_url == "https://nyaa.si/"


async def test_nyaa_default(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1755409")
    assert nyaa.title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"
    assert nyaa.submitter.name == "smol"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is False


async def test_nyaa_trusted(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1544043")
    assert nyaa.title == "[MTBB] I Want to Eat Your Pancreas (BD 1080p) | Kimi no Suizou wo Tabetai"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.is_remake is False
    assert nyaa.is_trusted is True
    assert nyaa.category == Category.ANIME_ENGLISH_TRANSLATED


async def test_nyaa_trusted_and_remake(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1694824")
    assert (
        nyaa.title
        == "[MiniMTBB] Sound! Euphonium the Movie: Our Promise: A Brand New Day (BD 1080p) | Hibike! Euphonium: Chikai no Finale"
    )
    assert nyaa.is_remake is True
    assert nyaa.is_trusted is False
    assert nyaa.submitter.is_trusted is True


async def test_nyaa_anon(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get(1765655)
    assert (
        nyaa.title
        == "[Kinoworm] Ascendance of a Bookworm P01v01-P05v08 + Fanbook v01-v03 + Royal Academy Stories First Year v01 + Short Story Collection v01 (J-Novel Club) (Premium)"
    )
    assert nyaa.url.__str__() == "https://nyaa.si/view/1765655"
    assert nyaa.information == "https://www.goodreads.com/series/220639-ascendance-of-a-bookworm-light-novel"
    assert nyaa.submitter.name == "Anonymous"
    assert nyaa.category == Category.LITERATURE_ENGLISH_TRANSLATED


async def test_nyaa_banned(async_nyaa_client: AsyncNyaa) -> None:
    # Thoughts and Prayers for our good friend succ_
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1422797")
    assert nyaa.title == "[succ_] Tsugumomo [BDRip 1920x1080 x264 FLAC]"
    assert nyaa.submitter.is_trusted is False
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 20


async def test_nyaa_banned_and_trusted(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/884488")
    assert nyaa.title == "[FMA1394] Fullmetal Alchemist (2003) [Dual Audio] [US BD] (batch)"
    assert nyaa.submitter.is_trusted is True
    assert nyaa.submitter.is_banned is True
    assert len(nyaa.torrent.files) == 51


async def test_nyaa_empty_info(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/5819")
    assert nyaa.information is None
    assert nyaa.description is not None


async def test_nyaa_empty_desc(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/76777")
    assert nyaa.information is not None
    assert nyaa.description is None


async def test_nyaa_empty_desc_info(async_nyaa_client: AsyncNyaa) -> None:
    nyaa = await async_nyaa_client.get("https://nyaa.si/view/1586776")
    assert nyaa.information is None
    assert nyaa.description is None


async def test_search(async_nyaa_client: AsyncNyaa) -> None:
    results = async_nyaa_client.search("smol shelter")
    async for result in results:
        assert result.title == "[smol] Shelter (2016) (BD 1080p HEVC FLAC) | Porter Robinson & Madeon - Shelter"
        break


async def test_nyaa_search_no_results(async_nyaa_client: AsyncNyaa) -> None:
    results = async_nyaa_client.search("akldlaskdjsaljdksd")  # 0 results
    assert [i async for i in results] == []
