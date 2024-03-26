from ._compat import StrEnum


class NyaaCategory(StrEnum):
    """Nyaa categories"""

    ANIME_MUSIC_VIDEO = "Anime - Anime Music Video"
    ANIME_ENGLISH_TRANSLATED = "Anime - English-translated"
    ANIME_NON_ENGLISH_TRANSLATED = "Anime - Non-English-translated"
    ANIME_RAW = "Anime - Raw"

    AUDIO_LOSSLESS = "Audio - Lossless"
    AUDIO_LOSSY = "Audio - Lossy"

    LITERATURE_ENGLISH_TRANSLATED = "Literature - English-translated"
    LITERATURE_NON_ENGLISH_TRANSLATED = "Literature - Non-English-translated"
    LITERATURE_RAW = "Literature - Raw"

    LIVE_ACTION_ENGLISH_TRANSLATED = "Live Action - English-translated"
    LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO = "Live Action - Idol/Promotional Video"
    LIVE_ACTION_NON_ENGLISH_TRANSLATED = "Live Action - Non-English-translated"
    LIVE_ACTION_RAW = "Live Action - Raw"

    PICTURES_GRAPHICS = "Pictures - Graphics"
    PICTURES_PHOTOS = "Pictures - Photos"

    SOFTWARE_APPLICATIONS = "Software - Applications"
    SOFTWARE_GAMES = "Software - Games"
