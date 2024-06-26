"""
This file saves the httpx.Response object returned by the GET method.
These saved responses are then used as mock responses in the tests.
"""

import pickle
from hashlib import sha256
from pathlib import Path

import httpx

links = [
    "https://nyaa.si/view/1422797",
    "https://nyaa.si/view/1544043",
    "https://nyaa.si/view/1586776",
    "https://nyaa.si/view/1694824",
    "https://nyaa.si/view/1755409",
    "https://nyaa.si/view/1765655",
    "https://nyaa.si/view/884488",
    # Called within .searc()
    "https://nyaa.si/view/1755409",
    "https://nyaa.si/view/1755409",
    "https://nyaa.si/view/1837736",
    "https://nyaa.si/view/1837420",
]

searches = {
    "akldlaskdjsaljdksd": "",
    "smol shelter": "https://nyaa.si?page=rss&f=0&c=0_0&q=smol%20shelter",
    '"[smol] Shelter (2016) (BD 1080p HEVC FLAC)"': "https://nyaa.si?page=rss&f=0&c=0_0&q=%22%5Bsmol%5D%20Shelter%20%282016%29%20%28BD%201080p%20HEVC%20FLAC%29%22",
    "vodes": "https://nyaa.si?page=rss&f=2&c=3_1&q=vodes",
    "mtbb": "https://nyaa.si?page=rss&f=0&c=1_2&q=mtbb",
}


def save_pages() -> None:
    for link in links:
        response = httpx.get(link)
        filename = Path(__file__).with_name(link.split("/")[-1])

        print(f"Saving {link} ({response}) to {filename}")

        with open(filename, "wb") as file:
            pickle.dump(response, file=file)

def save_torrents() -> None:
    for link in links:
        id = link.split("/")[-1]
        link = link.replace("view", "download") + ".torrent"
        response = httpx.get(link)
        filename = Path(__file__).with_name(f"{id}.torrent")

        print(f"Saving {link} ({response}) to {filename}")

        with open(filename, "wb") as file:
            pickle.dump(response, file=file)

def save_searches() -> None:
    for query, url in searches.items():

        response = httpx.get(url)
        name = sha256(query.encode()).hexdigest()
        filename = Path(__file__).with_name(f"{name}.search")

        print(f"Saving {url} ({response}) to {filename}")

        with open(filename, "wb") as file:
            pickle.dump(response, file=file)


if __name__ == "__main__":
    save_pages()
    save_torrents()
    save_searches()