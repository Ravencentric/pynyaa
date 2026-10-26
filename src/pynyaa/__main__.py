# Copyright (c) 2024-present Ravencentric
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import argparse
import datetime as dt
import enum
import json
from typing import Any

from ._client import Nyaa


def url(value: str) -> str:
    value = value.strip("/")
    match value.split("/"):
        case ["https:", "", "nyaa.si", "view", id] if id.isdigit():
            return value
        case _:
            raise argparse.ArgumentTypeError("expected a nyaa release url such as https://nyaa.si/view/123456")


def serialize(o: object) -> Any:
    match o:
        case dt.datetime():
            return o.isoformat()
        case enum.Enum(value=value):
            return value
        case _:
            raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def main() -> None:
    parser = argparse.ArgumentParser(prog="pynyaa", description="Fetch a nyaa release and print its metadata as JSON.")
    parser.add_argument("url", type=url, help="URL of the nyaa release")
    args = parser.parse_args()

    try:
        with Nyaa() as nyaa:
            release = nyaa.get(args.url)
    except Exception as error:  # noqa: BLE001
        parser.exit(1, f"Error: {error}\n")

    release = release.to_dict()
    payload = {
        **release,
        "torrent": {key: value for key, value in release["torrent"].items() if key != "data"},
    }
    print(json.dumps(payload, indent=2, default=serialize))


if __name__ == "__main__":
    main()
