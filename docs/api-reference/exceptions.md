`pynyaa` doesn't raise any custom exceptions of it's own. The two most likely errors you'll encounter will be either of these:

- `pynyaa.HTTPStatusError` - Alias for [`httpx.HTTPStatusError`](https://www.python-httpx.org/exceptions/). Raised if a request returns a non 2xx status code.
- `pynyaa.ValidationError` - Alias for [`pydantic.ValidationError`](https://docs.pydantic.dev/latest/errors/validation_errors/). Raised if an input is invalid.
