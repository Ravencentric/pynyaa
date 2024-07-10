<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pynyaa">
    <img src="https://raw.githubusercontent.com/Ravencentric/pynyaa/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    Turn nyaa.si torrent pages into neat Python objects
    <br/>
    <br/>
  </p>
</p>

<div align="center">

<a href="https://pypi.org/project/pynyaa/"><img src="https://img.shields.io/pypi/v/pynyaa" alt="PyPI - Version" ></a>
<img src="https://img.shields.io/pypi/pyversions/pynyaa" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/license/Ravencentric/pynyaa" alt="License">
<img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">

<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pynyaa/release.yml?" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pynyaa/test.yml?label=tests" alt="GitHub Workflow Status">
<a href="https://codecov.io/gh/Ravencentric/pynyaa"><img src="https://codecov.io/gh/Ravencentric/pynyaa/graph/badge.svg?token=9LZ2I4LDYT"/></a>

</div>

## Table Of Contents

* [About](#about)
* [Installation](#installation)
* [Usage](#usage)
* [Docs](#docs)
* [License](#license)

## About

- Supports both sync and async.
- Supports caching.
- Provides easy access to every field except comments (comments are useless).
- Parses both the nyaa page itself and it's accompanying `.torrent` file.

## Installation

`pynyaa` is available on [PyPI](https://pypi.org/project/pynyaa/), so you can simply use [pip](https://github.com/pypa/pip) to install it.

```sh
pip install pynyaa
```

## Usage
### API
```py
from pynyaa import Nyaa

# You can pass any httpx.Client() keyword argument to Nyaa()
headers = {"user-agent": "my-app/0.0.1"}
client = Nyaa(headers=headers)

nyaa = client.get("https://nyaa.si/view/1693817")  # Full URL
nyaa = client.get(1693817)  # Only the ID also works

print(nyaa.title)
#> [LYS1TH3A] Fate/stay night Heaven's Feel I. Presage Flower (2017) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
print(nyaa.submitter)
#> pog42
print(nyaa.torrent.files)
#> [File('Fate.stay.night.Heavens.Feel.I.Presage.Flower.2017.1080p.BluRay.Opus5.1.H.265-LYS1TH3A.mkv', size=12263052206)]
print(nyaa.torrent.infohash)
#> 6fdc0395a7fdde6ce3fb7f144b31f3cabdcbf537

torrents = client.search("LYS1TH3A")

for torrent in torrents:
    print(torrent)
    #> [LYS1TH3A] Fate/Zero Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
    #> [LYS1TH3A] Tamako Market Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
    #> [LYS1TH3A] Tamako Love Story (2014) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
```

### CLI
```shell
$ pynyaa https://nyaa.si/view/1839609 --indent 2
```
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
    "size": 1455173416,
    "infohash": "767d16e0aef5888b1a513a26709e963478ed4123",
    "piece_size": 1048576,
    "private": null,
    "trackers": [
      ["http://nyaa.tracker.wf:7777/announce"],
      ["wss://tracker.openwebtorrent.com"]
    ],
    "comment": "https://nyaa.si/view/1839609",
    "creation_date": "2024-06-30T07:42:07",
    "created_by": "NyaaV2",
    "source": null,
    "files": [
      {
        "file": "[SubsPlease] One Piece - 1110 (1080p) [B66CAB32].mkv",
        "size": 1455173416
      }
    ]
  }
}
```

# Docs

Checkout the complete documentation [here](https://pynyaa.ravencentric.cc/).

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pynyaa/blob/main/UNLICENSE) for more information.