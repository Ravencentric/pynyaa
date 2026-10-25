# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from dataclasses import fields

from typing_extensions import assert_type

from pynyaa._enums import Category, CategoryID, CategoryValue, ParentCategory, ParentCategoryID, ParentCategoryValue
from pynyaa._models import FileDict, NyaaRelease, NyaaReleaseDict, Submitter, SubmitterDict, Torrent, TorrentDict


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


def test_submitter_dict_typing() -> None:
    assert SubmitterDict.__required_keys__ == {field.name for field in fields(Submitter)}


def test_release_dict_typing() -> None:
    assert NyaaReleaseDict.__required_keys__ == {field.name for field in fields(NyaaRelease)}


def test_file_dict_typing() -> None:
    assert FileDict.__required_keys__ == {"path", "size"}


def test_torrent_dict_typing() -> None:
    assert TorrentDict.__required_keys__ == {field.name for field in fields(Torrent)} | {"size"}
