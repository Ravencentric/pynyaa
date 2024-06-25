from pynyaa import NyaaCategory, NyaaFilter


def test_nyaa_category_id_property() -> None:
    assert NyaaCategory.ANIME.id == "1_0"
    assert NyaaCategory.ANIME_MUSIC_VIDEO.id == "1_1"
    assert NyaaCategory.ANIME_ENGLISH_TRANSLATED.id == "1_2"
    assert NyaaCategory.ANIME_NON_ENGLISH_TRANSLATED.id == "1_3"
    assert NyaaCategory.ANIME_RAW.id == "1_4"

    assert NyaaCategory.AUDIO.id == "2_0"
    assert NyaaCategory.AUDIO_LOSSLESS.id == "2_1"
    assert NyaaCategory.AUDIO_LOSSY.id == "2_2"

    assert NyaaCategory.LITERATURE.id == "3_0"
    assert NyaaCategory.LITERATURE_ENGLISH_TRANSLATED.id == "3_1"
    assert NyaaCategory.LITERATURE_NON_ENGLISH_TRANSLATED.id == "3_2"
    assert NyaaCategory.LITERATURE_RAW.id == "3_3"

    assert NyaaCategory.LIVE_ACTION.id == "4_0"
    assert NyaaCategory.LIVE_ACTION_ENGLISH_TRANSLATED.id == "4_1"
    assert NyaaCategory.LIVE_ACTION_IDOL_PROMOTIONAL_VIDEO.id == "4_2"
    assert NyaaCategory.LIVE_ACTION_NON_ENGLISH_TRANSLATED.id == "4_3"
    assert NyaaCategory.LIVE_ACTION_RAW.id == "4_4"

    assert NyaaCategory.PICTURES.id == "5_0"
    assert NyaaCategory.PICTURES_GRAPHICS.id == "5_1"
    assert NyaaCategory.PICTURES_PHOTOS.id == "5_2"

    assert NyaaCategory.SOFTWARE.id == "6_0"
    assert NyaaCategory.SOFTWARE_APPLICATIONS.id == "6_1"
    assert NyaaCategory.SOFTWARE_GAMES.id == "6_2"


def test_nyaa_filter_enum_values() -> None:
    assert NyaaFilter.NO_FILTER.value == 0
    assert NyaaFilter.NO_REMAKES.value == 1
    assert NyaaFilter.TRUSTED_ONLY.value == 2
