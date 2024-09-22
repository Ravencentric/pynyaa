from __future__ import annotations

from typing import TYPE_CHECKING, overload

from pynyaa._compat import IntEnum, StrEnum
from pynyaa._types import CategoryID, CategoryLiteral, SortByLiteral

if TYPE_CHECKING:
    from typing_extensions import Self

CATEGORY_NAME_TO_ID_MAP: dict[str, CategoryID] = {
    # All, c=0_0
    "All": "0_0",
    # Anime, c=1_X
    "Anime": "1_0",
    "Anime - Anime Music Video": "1_1",
    "Anime - English-translated": "1_2",
    "Anime - Non-English-translated": "1_3",
    "Anime - Raw": "1_4",
    # Audio, c=2_X
    "Audio": "2_0",
    "Audio - Lossless": "2_1",
    "Audio - Lossy": "2_2",
    # Literature, c=3_X
    "Literature": "3_0",
    "Literature - English-translated": "3_1",
    "Literature - Non-English-translated": "3_2",
    "Literature - Raw": "3_3",
    # Live Action, c=4_X
    "Live Action": "4_0",
    "Live Action - English-translated": "4_1",
    "Live Action - Idol/Promotional Video": "4_2",
    "Live Action - Non-English-translated": "4_3",
    "Live Action - Raw": "4_4",
    # Pictures, c=5_X
    "Pictures": "5_0",
    "Pictures - Graphics": "5_1",
    "Pictures - Photos": "5_2",
    # Software, c=6_X
    "Software": "6_0",
    "Software - Applications": "6_1",
    "Software - Games": "6_2",
}

CATEGORY_ID_TO_NAME_MAP = {v: k for k, v in CATEGORY_NAME_TO_ID_MAP.items()}


class BaseStrEnum(StrEnum):
    """StrEnum with case-insensitive double-sided lookup"""

    @classmethod
    def _missing_(cls, value: object) -> Self:
        errmsg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            for member in cls:
                if (member.value.casefold() == value.casefold()) or (member.name.casefold() == value.casefold()):
                    return member
            raise ValueError(errmsg)
        raise ValueError(errmsg)


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

        Examples
        --------
        ```py
        >>> Category.ANIME_ENGLISH_TRANSLATED.id == "1_2"
        True
        >>> Category.ALL.id == "0_0"
        True
        ```
        """
        return CATEGORY_NAME_TO_ID_MAP[self.value]

    @property
    def parent(self) -> Self:
        """
        Returns the parent category.

        Examples
        --------
        ```py
        >>> Category.ANIME_ENGLISH_TRANSLATED.parent is Category.ANIME
        True
        >>> Category.ANIME.parent is Category.ANIME
        True
        ```
        """
        return self.get(self.value.split("-")[0].strip())

    @overload
    @classmethod
    def get(cls, key: CategoryLiteral, default: CategoryLiteral = "ALL") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: CategoryLiteral, default: str = "ALL") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: str, default: CategoryLiteral = "ALL") -> Self: ...

    @overload
    @classmethod
    def get(cls, key: str, default: str = "ALL") -> Self: ...

    @classmethod
    def get(cls, key: CategoryLiteral | str, default: CategoryLiteral | str = "ALL") -> Self:
        """
        Get the `Category` by its name, value, or id (case-insensitive).
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

        try:
            return cls(key)
        except ValueError:
            try:
                return cls(CATEGORY_ID_TO_NAME_MAP[key])  # type: ignore
            except KeyError:
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
        Get the `SortBy` by its name or value (case-insensitive).
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
        try:
            return cls(key)
        except ValueError:
            return cls(default)


class Filter(IntEnum):
    """Nyaa search filters"""

    NO_FILTER = 0
    NO_REMAKES = 1
    TRUSTED_ONLY = 2
