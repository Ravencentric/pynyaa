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
<img src="https://img.shields.io/github/license/Ravencentric/pynyaa" alt="License">
<img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
</p>

<p align="center">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pynyaa/release.yml?" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pynyaa/test.yml?label=tests" alt="GitHub Workflow Status">
<a href="https://codecov.io/gh/Ravencentric/pynyaa"><img src="https://codecov.io/gh/Ravencentric/pynyaa/graph/badge.svg?token=9LZ2I4LDYT"/></a>
</p>


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

`pynyaa` offers two main classes:

1. `Nyaa()` - Synchronous class

      ```py
      from pynyaa import Nyaa

      # You can pass any httpx.Client() keyword argument to Nyaa()
      headers = {"user-agent": "my-app/0.0.1"}
      client = Nyaa(headers=headers)

      nyaa = client.get("https://nyaa.si/view/1693817")  # Full URL
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


      # You can pass any httpx.AsyncClient() keyword argument to AsyncNyaa()
      headers = {"user-agent": "my-app/0.0.1"}
      client = AsyncNyaa(headers=headers)

      nyaa = asyncio.run(client.get("https://nyaa.si/view/1816037"))  # Full URL
      nyaa = asyncio.run(client.get(1794334)) # Only the ID also works

      print(nyaa.title)
      """
      [MTBB] K-ON! the Movie (2011) (BD 1080p)
      """
      print(nyaa.submitter)
      """
      Submitter(name='motbob', url=Url('https://nyaa.si/user/motbob'), is_trusted=True, is_banned=False)
      """
      print(nyaa.torrent.files)
      """
      [File('[MTBB] K-ON! the Movie (2011) (BD 1080p) [805DBF12].mkv', size=9697743037)]
      """
      print(nyaa.torrent.infohash)
      """
      31b11cc115eed6851277d6a3ca5e4ad119796526
      """
      ```


## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pynyaa/blob/main/UNLICENSE) for more information.