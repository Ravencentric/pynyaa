from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AnyUrl, UrlConstraints

MagnetUrl = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["magnet"])]
"""Url that only allows magnets."""

CategoryName = Literal[
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

SortName = Literal["comments", "size", "id", "datetime", "seeders", "leechers", "downloads"]
