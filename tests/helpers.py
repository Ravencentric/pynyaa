import pickle
from hashlib import sha256
from pathlib import Path

from httpx import Response

BASE_DIR = Path(__file__).parent / "__responses__"

# This workaround of loading a Response object and then re-casting is necessary because: https://github.com/lundberg/respx/issues/272


def get_response(nyaa_id: int) -> Response:
    """
    Grab the response object corresponding to nyaa_id,
    unpickle it, and cast it in a new Response object.
    """
    filename = BASE_DIR / str(nyaa_id)
    with open(filename, "rb") as file:
        response: Response = pickle.load(file)
        return Response(status_code=response.status_code, content=response.content)


def get_torrent(nyaa_id: int) -> Response:
    """
    Grab the response object of the torrent corresponding to nyaa_id,
    unpickle it, and cast it in a new Response object.
    """
    filename = BASE_DIR / f"{nyaa_id}.torrent"
    with open(filename, "rb") as file:
        response: Response = pickle.load(file)
        return Response(status_code=response.status_code, content=response.content)


def get_search(query: str) -> Response:
    """
    Grab the response object of a search string,
    unpickle it, and cast it in a new Response object.

    This search string is saved with it's SHA265 digest being the filename.
    """
    name = sha256(query.encode()).hexdigest()
    filename = BASE_DIR / f"{name}.search"
    with open(filename, "rb") as file:
        response: Response = pickle.load(file)
        return Response(status_code=response.status_code, content=response.content)
