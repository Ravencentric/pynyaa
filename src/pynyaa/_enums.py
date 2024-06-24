from ._compat import StrEnum

__all__ = ("NyaaCategory",)


class BaseStrEnumWithID(StrEnum):

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=1_2&q=`, where `c=1_2` is the ID for `Anime - English-translated`.
        """
        mapping = {
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


class Anime(BaseStrEnumWithID):
    ALL = "Anime"
    MUSIC_VIDEO = "Anime - Anime Music Video"
    ENGLISH_TRANSLATED = "Anime - English-translated"
    NON_ENGLISH_TRANSLATED = "Anime - Non-English-translated"
    RAW = "Anime - Raw"


class Audio(BaseStrEnumWithID):
    ALL = "Audio"
    LOSSLESS = "Audio - Lossless"
    LOSSY = "Audio - Lossy"


class Literature(BaseStrEnumWithID):
    ALL = "Literature"
    ENGLISH_TRANSLATED = "Literature - English-translated"
    NON_ENGLISH_TRANSLATED = "Literature - Non-English-translated"
    RAW = "Literature - Raw"


class LiveAction(BaseStrEnumWithID):
    ALL = "Live Action"
    ENGLISH_TRANSLATED = "Live Action - English-translated"
    IDOL_PROMOTIONAL_VIDEO = "Live Action - Idol/Promotional Video"
    NON_ENGLISH_TRANSLATED = "Live Action - Non-English-translated"
    RAW = "Live Action - Raw"


class Pictures(BaseStrEnumWithID):
    ALL = "Pictures"
    GRAPHICS = "Pictures - Graphics"
    PHOTOS = "Pictures - Photos"


class Software(BaseStrEnumWithID):
    ALL = "Software"
    APPLICATIONS = "Software - Applications"
    GAMES = "Software - Games"


class NyaaCategory:
    """This class holds enums for all the available categories on Nyaa.si"""

    ANIME = Anime
    AUDIO = Audio
    LITERATURE = Literature
    LIVE_ACTION = LiveAction
    PICTURES = Pictures
    SOFTWARE = Software
