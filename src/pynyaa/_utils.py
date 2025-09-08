from __future__ import annotations


def assert_type(obj: object, typ: type[object] | tuple[type[object], ...], param: str, /) -> None:  # pragma: no cover
    """Shortcut for `isinstance(obj, type)` with a nice error message."""
    if not isinstance(obj, typ):
        if isinstance(typ, tuple):
            match typ:
                case [one]:
                    expected = f"{one.__name__!r}"
                case [one, two]:
                    expected = f"{one.__name__!r} or {two.__name__!r}"
                case [*rest, last]:
                    names = (f"{obj.__name__!r}" for obj in rest)
                    expected = ", ".join(names) + f", or {last.__name__!r}"
        else:
            expected = f"{typ.__name__!r}"

        msg = f"Parameter '{param}' expected {expected}, but got {type(obj).__name__!r}."

        raise TypeError(msg)
