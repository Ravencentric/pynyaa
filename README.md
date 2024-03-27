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

<p align="center">
<a href="https://pypi.org/project/pynyaa/"><img src="https://img.shields.io/pypi/v/pynyaa" alt="PyPI - Version" ></a>
<img src="https://img.shields.io/pypi/pyversions/pynyaa" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pynyaa/release.yml?" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pynyaa/test.yml?label=tests" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/license/Ravencentric/pynyaa" alt="License">
<img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
</p>

## Table Of Contents

* [About](#about)
* [Installation](#installation)
* [Usage](#usage)
* [Docs](#docs)
* [License](#license)

## About

I needed to parse the details out of nyaa torrent pages for one of my personal projects so I initially wrote a little module to do just that but then decided it'll probably be useful as an independent library so here we are.

Some features:

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

`pynyaa` offers two main classes:

1. `Nyaa()` - Synchronous class

      ```py
      from pynyaa import Nyaa

      nyaa = Nyaa().get("https://nyaa.si/view/1693817")  # Full URL

      # You can also pass any httpx.Client() keyword argument to Nyaa()
      headers = {"user-agent": "my-app/0.0.1"}
      client = Nyaa(headers=headers)

      nyaa = client.get(1693817)  # Only the ID also works

      print(nyaa.title)
      """
      [LYS1TH3A] Fate/stay night Heaven's Feel I. Presage Flower (2017) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
      """
      print(nyaa.submitter)
      """
      Submitter(name='pog42', url=Url('https://nyaa.si/user/pog42'), is_trusted=False, is_banned=False)
      """
      print(nyaa.torrent.files)
      """
      [File('Fate.stay.night.Heavens.Feel.I.Presage.Flower.2017.1080p.BluRay.Opus5.1.H.265-LYS1TH3A.mkv', size=12263052206)]
      """
      print(nyaa.torrent.infohash)
      """
      6fdc0395a7fdde6ce3fb7f144b31f3cabdcbf537
      """
      ```

2. `AsyncNyaa()` - Asynchronous class

      ```py
      import asyncio
      from pynyaa import AsyncNyaa

      nyaa = asyncio.run(AsyncNyaa().get("https://nyaa.si/view/1794334")) # Full URL

      # You can also pass any httpx.AsyncClient() keyword argument to AsyncNyaa()
      headers = {"user-agent": "my-app/0.0.1"}
      client = AsyncNyaa(headers=headers)

      nyaa = asyncio.run(client.get(1794334)) # Only the ID also works

      print(nyaa.title)
      """
      [MTBB] The Dangers in My Heart S2 - 12 (WEB 1080p) | Boku no Kokoro no Yabai Yatsu S2
      """
      print(nyaa.submitter)
      """
      Submitter(name='motbob', url=Url('https://nyaa.si/user/motbob'), is_trusted=True, is_banned=False)
      """
      print(nyaa.torrent.files)
      """
      [File('[MTBB] The Dangers in My Heart S2 - 12 (WEB 1080p) [DE972341].mkv', size=758024360)]
      """
      print(nyaa.torrent.infohash)
      """
      fccba66ad15e9d3918fb965654b93679a6c59936
      """
      ```

# Docs

Checkout the complete API Reference [here](https://ravencentric.github.io/pynyaa/)

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pynyaa/blob/main/UNLICENSE) for more information.