"""Compatibility module to for older python versions"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from enum import IntEnum, StrEnum
else:
    from enum import IntEnum as IntEnumBase

    from strenum import StrEnum

    class IntEnum(IntEnumBase):
        def __str__(self) -> str:
            return str(self.value)


__all__ = ("StrEnum", "IntEnum")
