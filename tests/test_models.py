# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import datetime as dt
from dataclasses import replace

from pynyaa import Category, File, NyaaRelease, Submitter, Torrent
from pynyaa._models import NyaaReleaseDict


def test_to_dict() -> None:
    release = NyaaRelease(
        id=123,
        url="https://nyaa.si/view/123",
        title="Release title",
        category=Category.ANIME_RAW,
        submitter=Submitter(name="user", url="https://nyaa.si/user/user", is_trusted=True, is_banned=False),
        submitted_at=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        information="https://example.com",
        seeders=2,
        leechers=3,
        completed=4,
        is_trusted=False,
        is_remake=True,
        description="Description",
        torrent=Torrent(
            name="Release",
            filename="Release.torrent",
            files=(File("Release/a.mkv", size=7), File("Release/b.mkv", size=11)),
            data=b"raw torrent bytes",
            infohash="abc",
            url="https://nyaa.si/download/123.torrent",
            magnet="magnet:?xt=urn:btih:abc",
        ),
    )
    expected: NyaaReleaseDict = {
        "id": 123,
        "url": "https://nyaa.si/view/123",
        "title": "Release title",
        "category": Category.ANIME_RAW,
        "submitter": {"name": "user", "url": "https://nyaa.si/user/user", "is_trusted": True, "is_banned": False},
        "submitted_at": dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        "information": "https://example.com",
        "seeders": 2,
        "leechers": 3,
        "completed": 4,
        "is_trusted": False,
        "is_remake": True,
        "description": "Description",
        "torrent": {
            "name": "Release",
            "filename": "Release.torrent",
            "files": ({"path": "Release/a.mkv", "size": 7}, {"path": "Release/b.mkv", "size": 11}),
            "data": b"raw torrent bytes",
            "infohash": "abc",
            "url": "https://nyaa.si/download/123.torrent",
            "magnet": "magnet:?xt=urn:btih:abc",
            "size": 18,
        },
    }
    assert release.to_dict() == expected

    expected["submitter"] = None
    assert replace(release, submitter=None).to_dict() == expected
