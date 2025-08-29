from __future__ import annotations

import pytest

from pynyaa import Filter, ParentCategory, SortBy, TorrentCategory


def test_enum_errors() -> None:
    with pytest.raises(ValueError):
        Filter("asdadadsad")

    with pytest.raises(ValueError):
        Filter(999)

    with pytest.raises(ValueError):
        Filter(None)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        ParentCategory("asdadadsad")

    with pytest.raises(ValueError):
        ParentCategory(None)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        SortBy("asdadadsad")

    with pytest.raises(ValueError):
        SortBy(None)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        TorrentCategory("asdadadsad")

    with pytest.raises(ValueError):
        TorrentCategory(None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "category, expected_id",
    [
        (ParentCategory.ALL, "0_0"),
        (ParentCategory.ANIME, "1_0"),
        (TorrentCategory.ANIME_MUSIC_VIDEO, "1_1"),
        (TorrentCategory.ANIME_ENGLISH_TRANSLATED, "1_2"),
        (TorrentCategory.ANIME_NON_ENGLISH_TRANSLATED, "1_3"),
        (TorrentCategory.ANIME_RAW, "1_4"),
        (ParentCategory.AUDIO, "2_0"),
        (TorrentCategory.AUDIO_LOSSLESS, "2_1"),
        (TorrentCategory.AUDIO_LOSSY, "2_2"),
        (ParentCategory.LITERATURE, "3_0"),
        (TorrentCategory.LITERATURE_ENGLISH_TRANSLATED, "3_1"),
        (TorrentCategory.LITERATURE_NON_ENGLISH_TRANSLATED, "3_2"),
        (TorrentCategory.LITERATURE_RAW, "3_3"),
        (ParentCategory.LIVE_ACTION, "4_0"),
        (TorrentCategory.LIVE_ACTION_ENGLISH_TRANSLATED, "4_1"),
        (TorrentCategory.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO, "4_2"),
        (TorrentCategory.LIVE_ACTION_NON_ENGLISH_TRANSLATED, "4_3"),
        (TorrentCategory.LIVE_ACTION_RAW, "4_4"),
        (ParentCategory.PICTURES, "5_0"),
        (TorrentCategory.PICTURES_GRAPHICS, "5_1"),
        (TorrentCategory.PICTURES_PHOTOS, "5_2"),
        (ParentCategory.SOFTWARE, "6_0"),
        (TorrentCategory.SOFTWARE_APPLICATIONS, "6_1"),
        (TorrentCategory.SOFTWARE_GAMES, "6_2"),
    ],
)
def test_nyaa_category_id_property(category: ParentCategory | TorrentCategory, expected_id: str) -> None:
    assert category.id == expected_id


@pytest.mark.parametrize(
    "category, expected_parent",
    [
        (TorrentCategory.ANIME_MUSIC_VIDEO, ParentCategory.ANIME),
        (TorrentCategory.ANIME_ENGLISH_TRANSLATED, ParentCategory.ANIME),
        (TorrentCategory.ANIME_NON_ENGLISH_TRANSLATED, ParentCategory.ANIME),
        (TorrentCategory.ANIME_RAW, ParentCategory.ANIME),
        (TorrentCategory.AUDIO_LOSSLESS, ParentCategory.AUDIO),
        (TorrentCategory.AUDIO_LOSSY, ParentCategory.AUDIO),
        (TorrentCategory.LITERATURE_ENGLISH_TRANSLATED, ParentCategory.LITERATURE),
        (TorrentCategory.LITERATURE_NON_ENGLISH_TRANSLATED, ParentCategory.LITERATURE),
        (TorrentCategory.LITERATURE_RAW, ParentCategory.LITERATURE),
        (TorrentCategory.LIVE_ACTION_ENGLISH_TRANSLATED, ParentCategory.LIVE_ACTION),
        (TorrentCategory.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO, ParentCategory.LIVE_ACTION),
        (TorrentCategory.LIVE_ACTION_NON_ENGLISH_TRANSLATED, ParentCategory.LIVE_ACTION),
        (TorrentCategory.LIVE_ACTION_RAW, ParentCategory.LIVE_ACTION),
        (TorrentCategory.PICTURES_GRAPHICS, ParentCategory.PICTURES),
        (TorrentCategory.PICTURES_PHOTOS, ParentCategory.PICTURES),
        (TorrentCategory.SOFTWARE_APPLICATIONS, ParentCategory.SOFTWARE),
        (TorrentCategory.SOFTWARE_GAMES, ParentCategory.SOFTWARE),
    ],
)
def test_nyaa_category_parent_property(category: TorrentCategory, expected_parent: ParentCategory) -> None:
    assert category.parent == expected_parent


@pytest.mark.parametrize(
    "input_value, expected_category",
    [
        ("All", ParentCategory.ALL),
        ("all", ParentCategory.ALL),
        ("AUDIO", ParentCategory.AUDIO),
        ("3_0", ParentCategory.LITERATURE),
        ("Live_Action", ParentCategory.LIVE_ACTION),
        ("Pictures", ParentCategory.PICTURES),
        ("Software", ParentCategory.SOFTWARE),
        ("aNiMe", ParentCategory.ANIME),
    ],
)
def test_parent_category(input_value: str, expected_category: ParentCategory) -> None:
    assert ParentCategory(input_value) == expected_category


@pytest.mark.parametrize(
    "input_value, expected_category",
    [
        ("Anime - Anime Music Video", TorrentCategory.ANIME_MUSIC_VIDEO),
        ("Anime - English-translated", TorrentCategory.ANIME_ENGLISH_TRANSLATED),
        ("1_2", TorrentCategory.ANIME_ENGLISH_TRANSLATED),
        ("Anime - Non-English-translated", TorrentCategory.ANIME_NON_ENGLISH_TRANSLATED),
        ("Anime - Raw", TorrentCategory.ANIME_RAW),
        ("Audio - Lossless", TorrentCategory.AUDIO_LOSSLESS),
        ("Audio - Lossy", TorrentCategory.AUDIO_LOSSY),
        ("Literature - English-translated", TorrentCategory.LITERATURE_ENGLISH_TRANSLATED),
        ("Literature - Non-English-translated", TorrentCategory.LITERATURE_NON_ENGLISH_TRANSLATED),
        ("Literature - Raw", TorrentCategory.LITERATURE_RAW),
        ("Live Action - English-translated", TorrentCategory.LIVE_ACTION_ENGLISH_TRANSLATED),
        ("LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO", TorrentCategory.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO),
        ("Live Action - Non-English-translated", TorrentCategory.LIVE_ACTION_NON_ENGLISH_TRANSLATED),
        ("Live Action - Raw", TorrentCategory.LIVE_ACTION_RAW),
        ("Pictures - Graphics", TorrentCategory.PICTURES_GRAPHICS),
        ("Pictures - Photos", TorrentCategory.PICTURES_PHOTOS),
        ("Software - Applications", TorrentCategory.SOFTWARE_APPLICATIONS),
        ("Software - Games", TorrentCategory.SOFTWARE_GAMES),
        ("aUdIo - lOsSy", TorrentCategory.AUDIO_LOSSY),
        ("lIvE aCtIoN - eNgLiSh-TrAnSlAtEd", TorrentCategory.LIVE_ACTION_ENGLISH_TRANSLATED),
    ],
)
def test_torrent_category(input_value: str, expected_category: TorrentCategory) -> None:
    assert TorrentCategory(input_value) == expected_category


@pytest.mark.parametrize(
    "key, category",
    [
        ("0_0", ParentCategory.ALL),
        ("1_0", ParentCategory.ANIME),
        ("2_0", ParentCategory.AUDIO),
        ("3_0", ParentCategory.LITERATURE),
        ("4_0", ParentCategory.LIVE_ACTION),
        ("5_0", ParentCategory.PICTURES),
        ("6_0", ParentCategory.SOFTWARE),
    ],
)
def test_parent_category_with_id(key: str, category: ParentCategory) -> None:
    assert ParentCategory(key) == category


@pytest.mark.parametrize(
    "key, category",
    [
        ("1_1", TorrentCategory.ANIME_MUSIC_VIDEO),
        ("1_2", TorrentCategory.ANIME_ENGLISH_TRANSLATED),
        ("1_3", TorrentCategory.ANIME_NON_ENGLISH_TRANSLATED),
        ("1_4", TorrentCategory.ANIME_RAW),
        ("2_1", TorrentCategory.AUDIO_LOSSLESS),
        ("2_2", TorrentCategory.AUDIO_LOSSY),
        ("3_1", TorrentCategory.LITERATURE_ENGLISH_TRANSLATED),
        ("3_2", TorrentCategory.LITERATURE_NON_ENGLISH_TRANSLATED),
        ("3_3", TorrentCategory.LITERATURE_RAW),
        ("4_1", TorrentCategory.LIVE_ACTION_ENGLISH_TRANSLATED),
        ("4_2", TorrentCategory.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO),
        ("4_3", TorrentCategory.LIVE_ACTION_NON_ENGLISH_TRANSLATED),
        ("4_4", TorrentCategory.LIVE_ACTION_RAW),
        ("5_1", TorrentCategory.PICTURES_GRAPHICS),
        ("5_2", TorrentCategory.PICTURES_PHOTOS),
        ("6_1", TorrentCategory.SOFTWARE_APPLICATIONS),
        ("6_2", TorrentCategory.SOFTWARE_GAMES),
    ],
)
def test_nyaa_category_get_with_id(key: str, category: TorrentCategory) -> None:
    assert TorrentCategory(key) == category


@pytest.mark.parametrize(
    "input_value, expected_sort_by",
    [
        ("comments", SortBy.COMMENTS),
        ("size", SortBy.SIZE),
        ("id", SortBy.DATETIME),
        ("datetime", SortBy.DATETIME),
        ("seeders", SortBy.SEEDERS),
        ("leechers", SortBy.LEECHERS),
        ("downloads", SortBy.DOWNLOADS),
        ("COMMENTS", SortBy.COMMENTS),
        ("SeEdErS", SortBy.SEEDERS),
    ],
)
def test_sort_by(input_value: str, expected_sort_by: SortBy) -> None:
    assert SortBy(input_value) == expected_sort_by


@pytest.mark.parametrize(
    "input_value, expected_filter",
    [
        ("NO_filter", Filter.NO_FILTER),
        (0, Filter.NO_FILTER),
        ("NO_REMAKES", Filter.NO_REMAKES),
        (1, Filter.NO_REMAKES),
        ("trusted_only", Filter.TRUSTED_ONLY),
        (2, Filter.TRUSTED_ONLY),
    ],
)
def test_filter(input_value: str, expected_filter: Filter) -> None:
    assert Filter(input_value) == expected_filter
