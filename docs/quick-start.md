## Python

For quick, single interactions with `Nyaa.si` you can use the top-level convenience functions:

- `pynyaa.get`
- `pynyaa.search`

These helpers create a temporary [`pynyaa.Nyaa`][pynyaa.Nyaa] client under the hood for one-off requests and then close it automatically.

```py
import pynyaa

release = pynyaa.get("https://nyaa.si/view/1693817")  # Full URL
release = pynyaa.get(1693817)  # Only the ID also works

print(release.title)
# > [LYS1TH3A] Fate/stay night Heaven's Feel I. Presage Flower (2017) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
print(release.submitter)
# > pog42
print(release.torrent.infohash)
# > 6fdc0395a7fdde6ce3fb7f144b31f3cabdcbf537

releases = pynyaa.search("LYS1TH3A")

for release in releases:
    print(release)
    # > [LYS1TH3A] Fate/Zero Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
    # > [LYS1TH3A] Tamako Market Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
    # > [LYS1TH3A] Tamako Love Story (2014) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
```

#### Advanced

If you're doing anything more than quick experiments or one-off scripts, it's best to use the [`Nyaa`][pynyaa.Nyaa]/[`AsyncNyaa`][pynyaa.AsyncNyaa] client directly. They give you far more flexibility and control over the requests along with improved performance.

!!! note
    For more details, see the [HTTPX documentation](https://www.python-httpx.org/advanced/clients/#why-use-a-client) on clients.


Using the same example as above but with the `Nyaa` client:
```py
from pynyaa import Nyaa

with Nyaa() as nyaa:
    release = nyaa.get("https://nyaa.si/view/1693817")

    print(release.title)
    # > [LYS1TH3A] Fate/stay night Heaven's Feel I. Presage Flower (2017) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]

    releases = nyaa.search("LYS1TH3A")

    for release in releases:
        print(release)
        # > [LYS1TH3A] Fate/Zero Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
        # > [LYS1TH3A] Tamako Market Season 1 (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
        # > [LYS1TH3A] Tamako Love Story (2014) (BD 1080p HEVC x265 10-bit Opus) [Dual-Audio]
```

You can also pass your own instance of an [`httpx.Client`](https://www.python-httpx.org/api/#client) to the [`Nyaa`][pynyaa.Nyaa] client. This gives you complete control over the requests. For example, you can cache responses with [Hishel](https://hishel.com/httpx.html).

```py
from hishel import FilterPolicy, SyncSqliteStorage
from hishel.httpx import SyncCacheClient

from pynyaa import Nyaa

storage = SyncSqliteStorage(default_ttl=60)
client = SyncCacheClient(storage=storage, policy=FilterPolicy())

with Nyaa(client=client) as nyaa:
    release = nyaa.get("https://nyaa.si/view/1693817")  # First request
    release = nyaa.get("https://nyaa.si/view/1693817")  # Returns the cached result
```

## Command Line

Fetch a release and print its metadata as JSON:

```sh
pynyaa https://nyaa.si/view/1755409
pynyaa https://nyaa.si/view/1755409 > release.json
```
