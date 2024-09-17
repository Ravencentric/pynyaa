from __future__ import annotations

from typing import overload

from typing_extensions import Self

from pynyaa._compat import IntEnum, StrEnum
from pynyaa._types import CategoryID, CategoryLiteral, SortByLiteral
from pynyaa._utils import get_category_id_from_name


class BaseStrEnum(StrEnum):
    """StrEnum with case-insensitive lookup"""

    @classmethod
    def _missing_(cls, value: object) -> Self:
        for member in cls:
            if member.value.casefold() == str(value).casefold():
                return member
        message = f"'{value}' is not a valid {type(cls)}"
        raise ValueError(message)


class Category(BaseStrEnum):
    """Nyaa categories"""

    ALL = "All"

    ANIME = "Anime"
    ANIME_MUSIC_VIDEO = "Anime - Anime Music Video"
    ANIME_ENGLISH_TRANSLATED = "Anime - English-translated"
    ANIME_NON_ENGLISH_TRANSLATED = "Anime - Non-English-translated"
    ANIME_RAW = "Anime - Raw"

    AUDIO = "Audio"
    AUDIO_LOSSLESS = "Audio - Lossless"
    AUDIO_LOSSY = "Audio - Lossy"

    LITERATURE = "Literature"
    LITERATURE_ENGLISH_TRANSLATED = "Literature - English-translated"
    LITERATURE_NON_ENGLISH_TRANSLATED = "Literature - Non-English-translated"
    LITERATURE_RAW = "Literature - Raw"

    LIVE_ACTION = "Live Action"
    LIVE_ACTION_ENGLISH_TRANSLATED = "Live Action - English-translated"
    LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO = "Live Action - Idol/Promotional Video"
    LIVE_ACTION_NON_ENGLISH_TRANSLATED = "Live Action - Non-English-translated"
    LIVE_ACTION_RAW = "Live Action - Raw"

    PICTURES = "Pictures"
    PICTURES_GRAPHICS = "Pictures - Graphics"
    PICTURES_PHOTOS = "Pictures - Photos"

    SOFTWARE = "Software"
    SOFTWARE_APPLICATIONS = "Software - Applications"
    SOFTWARE_GAMES = "Software - Games"

    @property
    def id(self) -> CategoryID:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=1_2&q=`, where `c=1_2` is the ID for `Anime - English-translated`.
        """
        return get_category_id_from_name(self.value)

    @overload
    @classmethod
    def get(cls, key: CategoryLiteral, default: CategoryLiteral = "All") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: CategoryLiteral, default: str = "All") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: str, default: CategoryLiteral = "All") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: str, default: str = "All") -> Self: ...

    @classmethod
    def get(cls, key: CategoryLiteral | str, default: CategoryLiteral | str = "All") -> Self:
        """
        Get the `Category` by its name (case-insensitive).
        Return the default if the key is missing or invalid.

        Parameters
        ----------
        key : CategoryLiteral | str
            The key to retrieve.
        default : CategoryLiteral | str, optional
            The default value to return if the key is missing or invalid.

        Returns
        -------
        Category
            The `Category` corresponding to the key.
        """
        match key:
            case str():
                for category in cls:
                    if (category.value.casefold() == key.casefold()) or (category.name.casefold() == key.casefold()):
                        return category
                else:
                    return cls(default)
            case _:
                return cls(default)


class SortBy(BaseStrEnum):
    COMMENTS = "comments"
    SIZE = "size"
    DATETIME = "id"  # yea... https://nyaa.si/?s=id&o=desc
    SEEDERS = "seeders"
    LEECHERS = "leechers"
    DOWNLOADS = "downloads"

    @overload
    @classmethod
    def get(cls, key: SortByLiteral, default: SortByLiteral = "datetime") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: SortByLiteral, default: str = "datetime") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: str, default: SortByLiteral = "datetime") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: str, default: str = "datetime") -> Self: ...

    @classmethod
    def get(cls, key: SortByLiteral | str, default: SortByLiteral | str = "datetime") -> Self:
        """
        Get the `SortBy` by its name (case-insensitive).
        Return the default if the key is missing or invalid.

        Parameters
        ----------
        key : SortByLiteral | str
            The key to retrieve.
        default : SortByLiteral | str, optional
            The default value to return if the key is missing or invalid.

        Returns
        -------
        Category
            The `SortBy` corresponding to the key.
        """

        # "datetime" doesn't actually exist, it's just an alias for "id"
        default = "id" if default.casefold() == "datetime" else default.casefold()
        key = "id" if key.casefold() == "datetime" else key.casefold()

        match key:
            case str():
                for category in cls:
                    if (category.value.casefold() == key.casefold()) or (category.name.casefold() == key.casefold()):
                        return category
                else:
                    return cls(default)
            case _:
                return cls(default)


class Filter(IntEnum):
    """Nyaa search filters"""

    NO_FILTER = 0
    NO_REMAKES = 1
    TRUSTED_ONLY = 2
