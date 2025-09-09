from __future__ import annotations

import pytest

from pynyaa import Category, Filter, ParentCategory, SortBy


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
        Category("asdadadsad")

    with pytest.raises(ValueError):
        Category(None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("category", "expected_id", "expected_value"),
    [
        (ParentCategory.ALL, "0_0", "All"),
        (ParentCategory.ANIME, "1_0", "Anime"),
        (Category.ANIME_MUSIC_VIDEO, "1_1", "Anime - Anime Music Video"),
        (Category.ANIME_ENGLISH_TRANSLATED, "1_2", "Anime - English-translated"),
        (Category.ANIME_NON_ENGLISH_TRANSLATED, "1_3", "Anime - Non-English-translated"),
        (Category.ANIME_RAW, "1_4", "Anime - Raw"),
        (ParentCategory.AUDIO, "2_0", "Audio"),
        (Category.AUDIO_LOSSLESS, "2_1", "Audio - Lossless"),
        (Category.AUDIO_LOSSY, "2_2", "Audio - Lossy"),
        (ParentCategory.LITERATURE, "3_0", "Literature"),
        (Category.LITERATURE_ENGLISH_TRANSLATED, "3_1", "Literature - English-translated"),
        (Category.LITERATURE_NON_ENGLISH_TRANSLATED, "3_2", "Literature - Non-English-translated"),
        (Category.LITERATURE_RAW, "3_3", "Literature - Raw"),
        (ParentCategory.LIVE_ACTION, "4_0", "Live Action"),
        (Category.LIVE_ACTION_ENGLISH_TRANSLATED, "4_1", "Live Action - English-translated"),
        (Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO, "4_2", "Live Action - Idol/Promotional Video"),
        (Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED, "4_3", "Live Action - Non-English-translated"),
        (Category.LIVE_ACTION_RAW, "4_4", "Live Action - Raw"),
        (ParentCategory.PICTURES, "5_0", "Pictures"),
        (Category.PICTURES_GRAPHICS, "5_1", "Pictures - Graphics"),
        (Category.PICTURES_PHOTOS, "5_2", "Pictures - Photos"),
        (ParentCategory.SOFTWARE, "6_0", "Software"),
        (Category.SOFTWARE_APPLICATIONS, "6_1", "Software - Applications"),
        (Category.SOFTWARE_GAMES, "6_2", "Software - Games"),
    ],
)
def test_nyaa_category(category: ParentCategory | Category, expected_id: str, expected_value: str) -> None:
    assert category.id == expected_id
    assert category.value == expected_value
    assert category.value == str(category)


@pytest.mark.parametrize(
    ("category", "expected_parent"),
    [
        (Category.ANIME_MUSIC_VIDEO, ParentCategory.ANIME),
        (Category.ANIME_ENGLISH_TRANSLATED, ParentCategory.ANIME),
        (Category.ANIME_NON_ENGLISH_TRANSLATED, ParentCategory.ANIME),
        (Category.ANIME_RAW, ParentCategory.ANIME),
        (Category.AUDIO_LOSSLESS, ParentCategory.AUDIO),
        (Category.AUDIO_LOSSY, ParentCategory.AUDIO),
        (Category.LITERATURE_ENGLISH_TRANSLATED, ParentCategory.LITERATURE),
        (Category.LITERATURE_NON_ENGLISH_TRANSLATED, ParentCategory.LITERATURE),
        (Category.LITERATURE_RAW, ParentCategory.LITERATURE),
        (Category.LIVE_ACTION_ENGLISH_TRANSLATED, ParentCategory.LIVE_ACTION),
        (Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO, ParentCategory.LIVE_ACTION),
        (Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED, ParentCategory.LIVE_ACTION),
        (Category.LIVE_ACTION_RAW, ParentCategory.LIVE_ACTION),
        (Category.PICTURES_GRAPHICS, ParentCategory.PICTURES),
        (Category.PICTURES_PHOTOS, ParentCategory.PICTURES),
        (Category.SOFTWARE_APPLICATIONS, ParentCategory.SOFTWARE),
        (Category.SOFTWARE_GAMES, ParentCategory.SOFTWARE),
    ],
)
def test_nyaa_category_parent_property(category: Category, expected_parent: ParentCategory) -> None:
    assert category.parent == expected_parent


@pytest.mark.parametrize(
    ("input_value", "expected_category"),
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
    ("input_value", "expected_category"),
    [
        ("Anime - Anime Music Video", Category.ANIME_MUSIC_VIDEO),
        ("Anime - English-translated", Category.ANIME_ENGLISH_TRANSLATED),
        ("1_2", Category.ANIME_ENGLISH_TRANSLATED),
        ("Anime - Non-English-translated", Category.ANIME_NON_ENGLISH_TRANSLATED),
        ("Anime - Raw", Category.ANIME_RAW),
        ("Audio - Lossless", Category.AUDIO_LOSSLESS),
        ("Audio - Lossy", Category.AUDIO_LOSSY),
        ("Literature - English-translated", Category.LITERATURE_ENGLISH_TRANSLATED),
        ("Literature - Non-English-translated", Category.LITERATURE_NON_ENGLISH_TRANSLATED),
        ("Literature - Raw", Category.LITERATURE_RAW),
        ("Live Action - English-translated", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
        ("LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO", Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO),
        ("Live Action - Non-English-translated", Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED),
        ("Live Action - Raw", Category.LIVE_ACTION_RAW),
        ("Pictures - Graphics", Category.PICTURES_GRAPHICS),
        ("Pictures - Photos", Category.PICTURES_PHOTOS),
        ("Software - Applications", Category.SOFTWARE_APPLICATIONS),
        ("Software - Games", Category.SOFTWARE_GAMES),
        ("aUdIo - lOsSy", Category.AUDIO_LOSSY),
        ("lIvE aCtIoN - eNgLiSh-TrAnSlAtEd", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
    ],
)
def test_torrent_category(input_value: str, expected_category: Category) -> None:
    assert Category(input_value) == expected_category


@pytest.mark.parametrize(
    ("key", "category"),
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
    ("key", "category"),
    [
        ("1_1", Category.ANIME_MUSIC_VIDEO),
        ("1_2", Category.ANIME_ENGLISH_TRANSLATED),
        ("1_3", Category.ANIME_NON_ENGLISH_TRANSLATED),
        ("1_4", Category.ANIME_RAW),
        ("2_1", Category.AUDIO_LOSSLESS),
        ("2_2", Category.AUDIO_LOSSY),
        ("3_1", Category.LITERATURE_ENGLISH_TRANSLATED),
        ("3_2", Category.LITERATURE_NON_ENGLISH_TRANSLATED),
        ("3_3", Category.LITERATURE_RAW),
        ("4_1", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
        ("4_2", Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO),
        ("4_3", Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED),
        ("4_4", Category.LIVE_ACTION_RAW),
        ("5_1", Category.PICTURES_GRAPHICS),
        ("5_2", Category.PICTURES_PHOTOS),
        ("6_1", Category.SOFTWARE_APPLICATIONS),
        ("6_2", Category.SOFTWARE_GAMES),
    ],
)
def test_nyaa_category_get_with_id(key: str, category: Category) -> None:
    assert Category(key) == category


@pytest.mark.parametrize(
    ("input_value", "expected_sort_by"),
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
    ("input_value", "expected_filter"),
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
