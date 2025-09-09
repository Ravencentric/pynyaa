from __future__ import annotations

import enum
import sys
from typing import TYPE_CHECKING, Literal, TypeAlias

if sys.version_info > (3, 11):
    from enum import Enum, IntEnum, StrEnum
else:
    import enum
    from enum import Enum

    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return self.value

    class IntEnum(enum.IntEnum):
        def __str__(self) -> str:
            return str(self.value)


if TYPE_CHECKING:
    from typing_extensions import Self


class DoubleSidedStrEnum(StrEnum):
    """StrEnum with case-insensitive lookup by name and value."""

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            value = value.casefold().strip()
            for member in cls:
                if (value == member.value.casefold()) or (value == member.name.casefold()):
                    return member
            raise ValueError(msg)
        raise ValueError(msg)


ParentCategoryValue: TypeAlias = Literal["All", "Anime", "Audio", "Literature", "Live Action", "Pictures", "Software"]
ParentCategoryID: TypeAlias = Literal["0_0", "1_0", "2_0", "3_0", "4_0", "5_0", "6_0"]


class ParentCategory(enum.Enum):
    """
    Represents the top-level categories on Nyaa.
    This enum supports case-insensitive lookup by member name, value, or ID.

    Examples
    --------
    >>> ParentCategory("anime")
    <ParentCategory.ANIME: 'Anime'>

    >>> ParentCategory("Live_Action")
    <ParentCategory.LIVE_ACTION: 'Live Action'>

    >>> ParentCategory("3_0")
    <ParentCategory.LITERATURE: 'Literature'>

    """

    if TYPE_CHECKING:

        @property
        def value(self) -> ParentCategoryValue: ...

        def __init__(self, value: str) -> None:
            self._id: ParentCategoryID
    else:

        def __init__(self, value: str, id: str) -> None:
            self._value_ = value
            self._id = id

    ALL = "All", "0_0"
    ANIME = "Anime", "1_0"
    AUDIO = "Audio", "2_0"
    LITERATURE = "Literature", "3_0"
    LIVE_ACTION = "Live Action", "4_0"
    PICTURES = "Pictures", "5_0"
    SOFTWARE = "Software", "6_0"

    @property
    def id(self) -> ParentCategoryID:
        """
        Returns the ID of the category.

        Examples
        --------
        ```py
        >>> ParentCategory.ANIME.id == "1_0"
        True
        >>> ParentCategory.ALL.id == "0_0"
        True
        ```

        """
        return self._id

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            value = value.casefold().strip()
            for member in cls:
                if (value == member.value.casefold()) or (value == member.name.casefold()) or (value == member.id):
                    return member
            raise ValueError(msg)
        raise ValueError(msg)

    def __str__(self) -> str:
        return self.value


CategoryValue: TypeAlias = Literal[
    "Anime - Anime Music Video",
    "Anime - English-translated",
    "Anime - Non-English-translated",
    "Anime - Raw",
    "Audio - Lossless",
    "Audio - Lossy",
    "Literature - English-translated",
    "Literature - Non-English-translated",
    "Literature - Raw",
    "Live Action - English-translated",
    "Live Action - Idol/Promotional Video",
    "Live Action - Non-English-translated",
    "Live Action - Raw",
    "Pictures - Graphics",
    "Pictures - Photos",
    "Software - Applications",
    "Software - Games",
]

CategoryID: TypeAlias = Literal[
    "1_1",
    "1_2",
    "1_3",
    "1_4",
    "2_1",
    "2_2",
    "3_1",
    "3_2",
    "3_3",
    "4_1",
    "4_2",
    "4_3",
    "4_4",
    "5_1",
    "5_2",
    "6_1",
    "6_2",
]


class Category(enum.Enum):
    """
    Represents the categories to which a torrent on Nyaa belongs.
    This enum supports case-insensitive lookup by member name, value, or ID.

    Examples
    --------
    >>> Category("ANIME_RAW")
    <Category.ANIME_RAW: 'Anime - Raw'>

    >>> Category("Literature - English-translated")
    <Category.LITERATURE_ENGLISH_TRANSLATED: 'Literature - English-translated'>

    >>> Category("2_1")
    <Category.AUDIO_LOSSLESS: 'Audio - Lossless'>

    """

    if TYPE_CHECKING:

        @property
        def value(self) -> CategoryValue: ...

        def __init__(self, value: str) -> None:
            self._id: CategoryID
    else:

        def __init__(self, value: str, id: str) -> None:
            self._value_ = value
            self._id = id

    ANIME_MUSIC_VIDEO = "Anime - Anime Music Video", "1_1"
    ANIME_ENGLISH_TRANSLATED = "Anime - English-translated", "1_2"
    ANIME_NON_ENGLISH_TRANSLATED = "Anime - Non-English-translated", "1_3"
    ANIME_RAW = "Anime - Raw", "1_4"

    AUDIO_LOSSLESS = "Audio - Lossless", "2_1"
    AUDIO_LOSSY = "Audio - Lossy", "2_2"

    LITERATURE_ENGLISH_TRANSLATED = "Literature - English-translated", "3_1"
    LITERATURE_NON_ENGLISH_TRANSLATED = "Literature - Non-English-translated", "3_2"
    LITERATURE_RAW = "Literature - Raw", "3_3"

    LIVE_ACTION_ENGLISH_TRANSLATED = "Live Action - English-translated", "4_1"
    LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO = "Live Action - Idol/Promotional Video", "4_2"
    LIVE_ACTION_NON_ENGLISH_TRANSLATED = "Live Action - Non-English-translated", "4_3"
    LIVE_ACTION_RAW = "Live Action - Raw", "4_4"

    PICTURES_GRAPHICS = "Pictures - Graphics", "5_1"
    PICTURES_PHOTOS = "Pictures - Photos", "5_2"

    SOFTWARE_APPLICATIONS = "Software - Applications", "6_1"
    SOFTWARE_GAMES = "Software - Games", "6_2"

    @property
    def id(self) -> CategoryID:
        """
        Returns the ID of the category.

        Examples
        --------
        ```py
        >>> Category.ANIME_ENGLISH_TRANSLATED.id == "1_2"
        True
        ```

        """
        return self._id

    @property
    def parent(self) -> ParentCategory:
        """
        Returns the corresponding `ParentCategory` for this category.

        Examples
        --------
        ```py
        >>> Category.ANIME_ENGLISH_TRANSLATED.parent == ParentCategory.ANIME
        True
        ```

        """
        parent, _ = self.value.split(" - ")
        return ParentCategory(parent)

    def __str__(self) -> str:
        return self.value

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            value = value.casefold().strip()
            for member in cls:
                if (value == member.value.casefold()) or (value == member.name.casefold()) or (value == member.id):
                    return member
            raise ValueError(msg)
        raise ValueError(msg)


class SortBy(DoubleSidedStrEnum):
    COMMENTS = "comments"
    SIZE = "size"
    DATETIME = "id"  # yea... https://nyaa.si/?s=id&o=desc
    SEEDERS = "seeders"
    LEECHERS = "leechers"
    DOWNLOADS = "downloads"


class Order(DoubleSidedStrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class Filter(IntEnum):
    if TYPE_CHECKING:

        def __init__(self, value: str | int): ...

    NO_FILTER = 0
    NO_REMAKES = 1
    TRUSTED_ONLY = 2

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"
        if isinstance(value, str):
            for member in cls:
                if value.casefold().strip() == member.name.casefold():
                    return member
        raise ValueError(msg)
