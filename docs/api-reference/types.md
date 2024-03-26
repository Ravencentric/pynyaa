!!! note
    `pynyaa` didn't need any custom types beyond what came out of the box in [`pydantic`](https://docs.pydantic.dev/latest/) and [`torf`](https://torf.readthedocs.io/en/latest/), so it just re-exports the ones that are used:

    - [AnyUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.AnyUrl)
    - [HttpUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl)
    - [Torrent](https://torf.readthedocs.io/en/latest/#torf.Torrent)
    - [File](https://torf.readthedocs.io/en/latest/#torf.File)
    - [Filepath](https://torf.readthedocs.io/en/latest/#torf.Filepath)

::: pynyaa._types.HTTPXAsyncClientKwargs
::: pynyaa._types.HTTPXClientKwargs
