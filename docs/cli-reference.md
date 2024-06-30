# CLI

`pynyaa` offers a very simple command-line interface. This is mostly meant for quickly getting the JSON representation of a torrent page.

## Usage

| Command        | Description                                           |
|----------------|-------------------------------------------------------|
| `pynyaa <url>` | Fetches JSON representation of a Nyaa torrent page.   |

### Options
| Option                | Short Form | Type        | Default | Description                           |
|-----------------------|------------|-------------|---------|---------------------------------------|
| `--indent <level>`    | `-i`       | `int`       | `2`     | Indentation level for JSON output.    |
| `--include <keys...>` | `-inc`     | `list[str]` | `None`  | Keys to include in the JSON output.   |
| `--exclude <keys...>` | `-exc`     | `list[str]` | `None`  | Keys to exclude from the JSON output. |


## Examples

1. `$ pynyaa https://nyaa.si/view/1839609`

    ```json
    {
      "id": 1839609,
      "url": "https://nyaa.si/view/1839609",
      "title": "[SubsPlease] One Piece - 1110 (1080p) [B66CAB32].mkv",
      "category": "Anime - English-translated",
      "date": "2024-06-30T02:12:07Z",
      "submitter": {
        "name": "subsplease",
        "url": "https://nyaa.si/user/subsplease",
        "is_trusted": true,
        "is_banned": false
      },
      "information": "https://subsplease.org/",
      "seeders": 1998,
      "leechers": 106,
      "completed": 7736,
      "is_trusted": true,
      "is_remake": false,
      "description": "...",
      "torrent_file": "https://nyaa.si/download/1839609.torrent",
      "magnet": "magnet:?xt=urn:btih:...&dn=...",
      "torrent": {
        "name": "[SubsPlease] One Piece - 1110 (1080p) [B66CAB32].mkv",
        "trackers": [
          ["http://nyaa.tracker.wf:7777/announce"],
          ["wss://tracker.openwebtorrent.com"],
          ["udp://open.stealth.si:80/announce"]
        ],
        "comment": "https://nyaa.si/view/1839609",
        "creation_date": "2024-06-30T07:42:07",
        "created_by": "NyaaV2",
        "piece_size": 1048576
      }
    }
    ```

2. `$ pynyaa https://nyaa.si/view/1839609 --include url title category date`

    ```json
    {
      "url": "https://nyaa.si/view/1839609",
      "title": "[SubsPlease] One Piece - 1110 (1080p) [B66CAB32].mkv",
      "category": "Anime - English-translated",
      "date": "2024-06-30T02:12:07Z"
    }
    ```


3. `$ pynyaa https://nyaa.si/view/1839609 --exclude description magnet torrent`

    ```json
    {
      "id": 1839609,
      "url": "https://nyaa.si/view/1839609",
      "title": "[SubsPlease] One Piece - 1110 (1080p) [B66CAB32].mkv",
      "category": "Anime - English-translated",
      "date": "2024-06-30T02:12:07Z",
      "submitter": {
        "name": "subsplease",
        "url": "https://nyaa.si/user/subsplease",
        "is_trusted": true,
        "is_banned": false
      },
      "information": "https://subsplease.org/",
      "seeders": 1998,
      "leechers": 106,
      "completed": 7736,
      "is_trusted": true,
      "is_remake": false,
      "torrent_file": "https://nyaa.si/download/1839609.torrent"
    }
    ```