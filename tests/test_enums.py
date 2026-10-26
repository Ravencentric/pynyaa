# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import pytest

from pynyaa import Category, Filter, ParentCategory, SortBy


def test_enum_errors() -> None:
    with pytest.raises(ValueError):
        Filter("asdadadsad")

    with pytest.raises(ValueError):
        Filter(999)

    with pytest.raises(ValueError):
        Filter(None)

    with pytest.raises(ValueError):
        ParentCategory("asdadadsad")

    with pytest.raises(ValueError):
        ParentCategory(None)

    with pytest.raises(ValueError):
        SortBy("asdadadsad")

    with pytest.raises(ValueError):
        SortBy(None)

    with pytest.raises(ValueError):
        Category("asdadadsad")

    with pytest.raises(ValueError):
        Category(None)


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
    cls = type(category)
    assert cls(expected_id) is category
    assert cls(f"  {expected_value.swapcase()}  ") is category
    assert cls(f"  {category.name.lower()}") is category


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
