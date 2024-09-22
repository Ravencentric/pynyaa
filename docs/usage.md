#### Quick Start

```py
import pynyaa

nyaa = pynyaa.get("https://nyaa.si/view/1693817")  # Full URL
nyaa = pynyaa.get(1693817)  # Only the ID also works

print(nyaa.title)
#> [LYS1TH3A] Fate/stay night Heaven's Feel I. Presage Flower (2017) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
print(nyaa.submitter)
#> pog42
print(nyaa.torrent.files)
#> [File('Fate.stay.night.Heavens.Feel.I.Presage.Flower.2017.1080p.BluRay.Opus5.1.H.265-LYS1TH3A.mkv', size=12263052206)]
print(nyaa.torrent.infohash)
#> 6fdc0395a7fdde6ce3fb7f144b31f3cabdcbf537

torrents = pynyaa.search("LYS1TH3A")

for torrent in torrents:
    print(torrent)
    #> [LYS1TH3A] Fate/Zero Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
    #> [LYS1TH3A] Tamako Market Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
    #> [LYS1TH3A] Tamako Love Story (2014) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
```

#### Advanced

If you're doing anything more than quick experiments or one-off scripts, it's best to use the [`Nyaa`][pynyaa.Nyaa]/[`AsyncNyaa`][pynyaa.AsyncNyaa] client directly. They give you far more flexibility and control over the requests along with improved performance.

!!! note
    For more details, see the [HTTPX documentation](https://www.python-httpx.org/advanced/clients/#why-use-a-client) on clients.


Using the same example as above but with the `Nyaa` client:
```py
from pynyaa import Nyaa

with Nyaa() as client:
    nyaa = client.get("https://nyaa.si/view/1693817")

    print(nyaa.title)
    #> [LYS1TH3A] Fate/stay night Heaven's Feel I. Presage Flower (2017) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]

    torrents = client.search("LYS1TH3A")

    for torrent in torrents:
        print(torrent)
        #> [LYS1TH3A] Fate/Zero Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
        #> [LYS1TH3A] Tamako Market Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
        #> [LYS1TH3A] Tamako Love Story (2014) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
```

You can also pass your own instance of an [`httpx.Client`](https://www.python-httpx.org/api/#client) to the [`Nyaa`][pynyaa.Nyaa] client. This gives you complete control over the requests. For example, we can use this to quickly implement aggressive caching with [`hishel`](https://github.com/karpetrosyan/hishel):

```py
from hishel import CacheClient, Controller, InMemoryStorage

from pynyaa import Nyaa

storage = InMemoryStorage(capacity=256)
controller = Controller(force_cache=True)

with Nyaa(client=CacheClient(storage=storage, controller=controller)) as client:
    nyaa1 = client.get("https://nyaa.si/view/1693817")  # First request
    nyaa2 = client.get("https://nyaa.si/view/1693817")  # Returns the cached result
```
