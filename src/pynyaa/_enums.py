from ._compat import IntEnum, StrEnum


class NyaaCategory(StrEnum):
    """Nyaa categories"""

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
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=1_2&q=`, where `c=1_2` is the ID for `Anime - English-translated`.
        """
        mapping = {
            # All, c=0_0
            "All categories": "0_0",
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

        return mapping.get(self.value, "0_0")


class NyaaFilter(IntEnum):
    """Nyaa search filters"""

    NO_FILTER = 0
    NO_REMAKES = 1
    TRUSTED_ONLY = 2
