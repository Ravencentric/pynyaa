from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from pynyaa._types import CategoryID


def _get_category_id_from_name(key: str) -> CategoryID:
    mapping: dict[str, CategoryID] = {
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
    return mapping[key]
