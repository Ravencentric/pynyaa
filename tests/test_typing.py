from __future__ import annotations

import typing

from typing_extensions import assert_type

from pynyaa._enums import Category, CategoryID, CategoryValue, ParentCategory, ParentCategoryID, ParentCategoryValue


def test_parent_category_typing() -> None:
    assert_type(ParentCategory.ANIME.id, ParentCategoryID)
    assert_type(ParentCategory.ANIME.value, ParentCategoryValue)
    assert typing.get_args(ParentCategoryID) == tuple(member.id for member in ParentCategory)
    assert typing.get_args(ParentCategoryValue) == tuple(member.value for member in ParentCategory)


def test_category_typing() -> None:
    assert_type(Category.ANIME_ENGLISH_TRANSLATED.id, CategoryID)
    assert_type(Category.ANIME_ENGLISH_TRANSLATED.value, CategoryValue)
    assert typing.get_args(CategoryID) == tuple(member.id for member in Category)
    assert typing.get_args(CategoryValue) == tuple(member.value for member in Category)
