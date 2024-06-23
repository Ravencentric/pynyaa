from ._compat import StrEnum

__all__ = ("NyaaCategory",)


class Anime(StrEnum):
    ALL = "Anime"
    MUSIC_VIDEO = "Anime - Anime Music Video"
    ENGLISH_TRANSLATED = "Anime - English-translated"
    NON_ENGLISH_TRANSLATED = "Anime - Non-English-translated"
    RAW = "Anime - Raw"

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=1_2&q=`, where `c=1_2` is the ID for `Anime - English-translated`.
        """
        mapping = {
            "Anime": "1_0",
            "Anime - Anime Music Video": "1_1",
            "Anime - English-translated": "1_2",
            "Anime - Non-English-translated": "1_3",
            "Anime - Raw": "1_4",
        }

        return mapping[self.value]


class Audio(StrEnum):
    ALL = "Audio"
    LOSSLESS = "Audio - Lossless"
    LOSSY = "Audio - Lossy"

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=2_1&q=`, where `c=2_1` is the ID for `Audio - Lossless`.
        """
        mapping = {
            "Audio": "2_0",
            "Audio - Lossless": "2_1",
            "Audio - Lossy": "2_2",
        }

        return mapping[self.value]


class Literature(StrEnum):
    ALL = "Literature"
    ENGLISH_TRANSLATED = "Literature - English-translated"
    NON_ENGLISH_TRANSLATED = "Literature - Non-English-translated"
    RAW = "Literature - Raw"

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=3_1&q=`, where `c=3_1` is the ID for `Literature - English-translated`.
        """
        mapping = {
            "Literature": "3_0",
            "Literature - English-translated": "3_1",
            "Literature - Non-English-translated": "3_2",
            "Literature - Raw": "3_3",
        }

        return mapping[self.value]


class LiveAction(StrEnum):
    ALL = "Live Action"
    ENGLISH_TRANSLATED = "Live Action - English-translated"
    IDOL_PROMOTIONAL_VIDEO = "Live Action - Idol/Promotional Video"
    NON_ENGLISH_TRANSLATED = "Live Action - Non-English-translated"
    RAW = "Live Action - Raw"

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=4_1&q=`, where `c=4_1` is the ID for `Live Action - English-translated`.
        """
        mapping = {
            "Live Action": "4_0",
            "Live Action - English-translated": "4_1",
            "Live Action - Idol/Promotional Video": "4_2",
            "Live Action - Non-English-translated": "4_3",
            "Live Action - Raw": "4_4",
        }

        return mapping[self.value]


class Pictures(StrEnum):
    ALL = "Pictures"
    GRAPHICS = "Pictures - Graphics"
    PHOTOS = "Pictures - Photos"

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=5_1&q=`, where `c=5_1` is the ID for `Pictures - Graphics`.
        """
        mapping = {
            "Pictures": "5_0",
            "Pictures - Graphics": "5_1",
            "Pictures - Photos": "5_2",
        }

        return mapping[self.value]


class Software(StrEnum):
    ALL = "Software"
    APPLICATIONS = "Software - Applications"
    GAMES = "Software - Games"

    @property
    def id(self) -> str:
        """
        Returns the ID of the category.

        This ID corresponds to the category as seen in the URL
        `https://nyaa.si/?f=0&c=6_1&q=`, where `c=6_1` is the ID for `Software - Applications`.
        """
        mapping = {
            "Software": "6_0",
            "Software - Applications": "6_1",
            "Software - Games": "6_2",
        }

        return mapping[self.value]

class NyaaCategory:
    """This class holds all the available categories on Nyaa.si"""

    ANIME = Anime
    AUDIO = Audio
    LITERATURE = Literature
    LIVE_ACTION = LiveAction
    PICTURES = Pictures
    SOFTWARE = Software
