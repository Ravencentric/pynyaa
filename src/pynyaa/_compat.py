"""Compatibility module to for older python versions"""

import sys

if sys.version_info >= (3, 11):
    from enum import IntEnum, StrEnum
else:
    from enum import IntEnum as IntEnumBase

    from strenum import StrEnum

    class IntEnum(IntEnumBase):
        def __str__(self) -> str:
            return str(self.value)


if sys.version_info >= (3, 10):
    from importlib import metadata
else:
    import importlib_metadata as metadata

__all__ = ("metadata", "StrEnum", "IntEnum")
