from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Literal, Union

from pydantic import AfterValidator, AnyUrl, UrlConstraints

UTCDateTime = Annotated[datetime, AfterValidator(lambda dt: dt.astimezone(timezone.utc))]
"""datetime.datetime that's always in UTC."""

MagnetUrl = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["magnet"])]
"""Url that only allows magnets."""

CategoryName = Literal[
    "ALL",
    "ANIME",
    "ANIME_MUSIC_VIDEO",
    "ANIME_ENGLISH_TRANSLATED",
    "ANIME_NON_ENGLISH_TRANSLATED",
    "ANIME_RAW",
    "AUDIO",
    "AUDIO_LOSSLESS",
    "AUDIO_LOSSY",
    "LITERATURE",
    "LITERATURE_ENGLISH_TRANSLATED",
    "LITERATURE_NON_ENGLISH_TRANSLATED",
    "LITERATURE_RAW",
    "LIVE_ACTION",
    "LIVE_ACTION_ENGLISH_TRANSLATED",
    "LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO",
    "LIVE_ACTION_NON_ENGLISH_TRANSLATED",
    "LIVE_ACTION_RAW",
    "PICTURES",
    "PICTURES_GRAPHICS",
    "PICTURES_PHOTOS",
    "SOFTWARE",
    "SOFTWARE_APPLICATIONS",
    "SOFTWARE_GAMES",
]

CategoryValue = Literal[
    "All",
    "Anime",
    "Anime - Anime Music Video",
    "Anime - English-translated",
    "Anime - Non-English-translated",
    "Anime - Raw",
    "Audio",
    "Audio - Lossless",
    "Audio - Lossy",
    "Literature",
    "Literature - English-translated",
    "Literature - Non-English-translated",
    "Literature - Raw",
    "Live Action",
    "Live Action - English-translated",
    "Live Action - Idol/Promotional Video",
    "Live Action - Non-English-translated",
    "Live Action - Raw",
    "Pictures",
    "Pictures - Graphics",
    "Pictures - Photos",
    "Software",
    "Software - Applications",
    "Software - Games",
]

CategoryID = Literal[
    "0_0",
    "1_0",
    "1_1",
    "1_2",
    "1_3",
    "1_4",
    "2_0",
    "2_1",
    "2_2",
    "3_0",
    "3_1",
    "3_2",
    "3_3",
    "4_0",
    "4_1",
    "4_2",
    "4_3",
    "4_4",
    "5_0",
    "5_1",
    "5_2",
    "6_0",
    "6_1",
    "6_2",
]

CategoryLiteral = Union[CategoryName, CategoryValue, CategoryID]

SortByLiteral = Literal["comments", "size", "id", "datetime", "seeders", "leechers", "downloads"]
