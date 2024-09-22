from __future__ import annotations

import pytest

from pynyaa import Category, Filter, SortBy


def test_category_value_error() -> None:
    with pytest.raises(ValueError):
        Category.get("asdadadsad", "invalid default")


def test_sortby_value_error() -> None:
    with pytest.raises(ValueError):
        SortBy.get("asdadadsad", "invalid default")


@pytest.mark.parametrize(
    "category, expected_id",
    [
        (Category.ALL, "0_0"),
        (Category.ANIME, "1_0"),
        (Category.ANIME_MUSIC_VIDEO, "1_1"),
        (Category.ANIME_ENGLISH_TRANSLATED, "1_2"),
        (Category.ANIME_NON_ENGLISH_TRANSLATED, "1_3"),
        (Category.ANIME_RAW, "1_4"),
        (Category.AUDIO, "2_0"),
        (Category.AUDIO_LOSSLESS, "2_1"),
        (Category.AUDIO_LOSSY, "2_2"),
        (Category.LITERATURE, "3_0"),
        (Category.LITERATURE_ENGLISH_TRANSLATED, "3_1"),
        (Category.LITERATURE_NON_ENGLISH_TRANSLATED, "3_2"),
        (Category.LITERATURE_RAW, "3_3"),
        (Category.LIVE_ACTION, "4_0"),
        (Category.LIVE_ACTION_ENGLISH_TRANSLATED, "4_1"),
        (Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO, "4_2"),
        (Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED, "4_3"),
        (Category.LIVE_ACTION_RAW, "4_4"),
        (Category.PICTURES, "5_0"),
        (Category.PICTURES_GRAPHICS, "5_1"),
        (Category.PICTURES_PHOTOS, "5_2"),
        (Category.SOFTWARE, "6_0"),
        (Category.SOFTWARE_APPLICATIONS, "6_1"),
        (Category.SOFTWARE_GAMES, "6_2"),
    ],
)
def test_nyaa_category_id_property(category, expected_id):
    assert category.id == expected_id


@pytest.mark.parametrize(
    "category, expected_parent",
    [
        (Category.ALL, Category.ALL),
        (Category.ANIME, Category.ANIME),
        (Category.ANIME_MUSIC_VIDEO, Category.ANIME),
        (Category.ANIME_ENGLISH_TRANSLATED, Category.ANIME),
        (Category.ANIME_NON_ENGLISH_TRANSLATED, Category.ANIME),
        (Category.ANIME_RAW, Category.ANIME),
        (Category.AUDIO, Category.AUDIO),
        (Category.AUDIO_LOSSLESS, Category.AUDIO),
        (Category.AUDIO_LOSSY, Category.AUDIO),
        (Category.LITERATURE, Category.LITERATURE),
        (Category.LITERATURE_ENGLISH_TRANSLATED, Category.LITERATURE),
        (Category.LITERATURE_NON_ENGLISH_TRANSLATED, Category.LITERATURE),
        (Category.LITERATURE_RAW, Category.LITERATURE),
        (Category.LIVE_ACTION, Category.LIVE_ACTION),
        (Category.LIVE_ACTION_ENGLISH_TRANSLATED, Category.LIVE_ACTION),
        (Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO, Category.LIVE_ACTION),
        (Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED, Category.LIVE_ACTION),
        (Category.LIVE_ACTION_RAW, Category.LIVE_ACTION),
        (Category.PICTURES, Category.PICTURES),
        (Category.PICTURES_GRAPHICS, Category.PICTURES),
        (Category.PICTURES_PHOTOS, Category.PICTURES),
        (Category.SOFTWARE, Category.SOFTWARE),
        (Category.SOFTWARE_APPLICATIONS, Category.SOFTWARE),
        (Category.SOFTWARE_GAMES, Category.SOFTWARE),
    ],
)
def test_nyaa_category_parent_property(category, expected_parent):
    assert category.parent is expected_parent


@pytest.mark.parametrize(
    "input_value, expected_category",
    [
        ("All", Category.ALL),
        ("all", Category.ALL),
        ("Anime", Category.ANIME),
        ("Anime - Anime Music Video", Category.ANIME_MUSIC_VIDEO),
        ("Anime - English-translated", Category.ANIME_ENGLISH_TRANSLATED),
        ("Anime - Non-English-translated", Category.ANIME_NON_ENGLISH_TRANSLATED),
        ("Anime - Raw", Category.ANIME_RAW),
        ("Audio", Category.AUDIO),
        ("Audio - Lossless", Category.AUDIO_LOSSLESS),
        ("Audio - Lossy", Category.AUDIO_LOSSY),
        ("Literature", Category.LITERATURE),
        ("Literature - English-translated", Category.LITERATURE_ENGLISH_TRANSLATED),
        ("Literature - Non-English-translated", Category.LITERATURE_NON_ENGLISH_TRANSLATED),
        ("Literature - Raw", Category.LITERATURE_RAW),
        ("Live Action", Category.LIVE_ACTION),
        ("Live Action - English-translated", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
        ("Live Action - Idol/Promotional Video", Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO),
        ("Live Action - Non-English-translated", Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED),
        ("Live Action - Raw", Category.LIVE_ACTION_RAW),
        ("Pictures", Category.PICTURES),
        ("Pictures - Graphics", Category.PICTURES_GRAPHICS),
        ("Pictures - Photos", Category.PICTURES_PHOTOS),
        ("Software", Category.SOFTWARE),
        ("Software - Applications", Category.SOFTWARE_APPLICATIONS),
        ("Software - Games", Category.SOFTWARE_GAMES),
        ("Invalid Category", Category.ALL),
        ("aNiMe", Category.ANIME),
        ("aUdIo - lOsSy", Category.AUDIO_LOSSY),
        ("lIvE aCtIoN - eNgLiSh-TrAnSlAtEd", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
    ],
)
def test_nyaa_category_get(input_value, expected_category):
    assert Category.get(input_value) == expected_category


@pytest.mark.parametrize(
    "key, category",
    [
        ("0_0", Category.ALL),
        ("1_0", Category.ANIME),
        ("1_1", Category.ANIME_MUSIC_VIDEO),
        ("1_2", Category.ANIME_ENGLISH_TRANSLATED),
        ("1_3", Category.ANIME_NON_ENGLISH_TRANSLATED),
        ("1_4", Category.ANIME_RAW),
        ("2_0", Category.AUDIO),
        ("2_1", Category.AUDIO_LOSSLESS),
        ("2_2", Category.AUDIO_LOSSY),
        ("3_0", Category.LITERATURE),
        ("3_1", Category.LITERATURE_ENGLISH_TRANSLATED),
        ("3_2", Category.LITERATURE_NON_ENGLISH_TRANSLATED),
        ("3_3", Category.LITERATURE_RAW),
        ("4_0", Category.LIVE_ACTION),
        ("4_1", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
        ("4_2", Category.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO),
        ("4_3", Category.LIVE_ACTION_NON_ENGLISH_TRANSLATED),
        ("4_4", Category.LIVE_ACTION_RAW),
        ("5_0", Category.PICTURES),
        ("5_1", Category.PICTURES_GRAPHICS),
        ("5_2", Category.PICTURES_PHOTOS),
        ("6_0", Category.SOFTWARE),
        ("6_1", Category.SOFTWARE_APPLICATIONS),
        ("6_2", Category.SOFTWARE_GAMES),
        ("6_9", Category.ALL),
        ("9_9", Category.ALL),
        ("-1_-1", Category.ALL),
    ],
)
def test_nyaa_category_get_with_id(key, category):
    assert Category.get(key) is category


@pytest.mark.parametrize(
    "input_value, default, expected_category",
    [
        (12345, "Anime", Category.ANIME),
        (None, "Software", Category.SOFTWARE),
        (None, "aLL", Category.ALL),
        ("test", "lIvE aCtIoN - eNgLiSh-TrAnSlAtEd", Category.LIVE_ACTION_ENGLISH_TRANSLATED),
    ],
)
def test_nyaa_category_get_with_default(input_value, default, expected_category):
    assert Category.get(input_value, default=default) == expected_category


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
        ("random", SortBy.DATETIME),
        ("", SortBy.DATETIME),
        ("COMMENTS", SortBy.COMMENTS),
        ("SeEdErS", SortBy.SEEDERS),
    ],
)
def test_sort_by_get(input_value, expected_sort_by):
    assert SortBy.get(input_value) == expected_sort_by


@pytest.mark.parametrize(
    "input_value, default, expected_sort_by",
    [
        ("invalid", "comments", SortBy.COMMENTS),
        (12345, "size", SortBy.SIZE),
        (None, "iD", SortBy.DATETIME),
        ("SnEEders", "dateTIME", SortBy.DATETIME),
    ],
)
def test_sort_by_get_with_default(input_value, default, expected_sort_by):
    assert SortBy.get(input_value, default=default) == expected_sort_by


def test_nyaa_filter_enum_values() -> None:
    assert Filter.NO_FILTER == 0
    assert Filter.NO_REMAKES == 1
    assert Filter.TRUSTED_ONLY == 2
