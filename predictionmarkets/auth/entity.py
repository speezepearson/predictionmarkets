from __future__ import annotations
import hashlib
import dataclasses
import typing as t

from .authenticator import Authenticator

@dataclasses.dataclass(frozen=True)
class Entity:
    authenticator: Authenticator

__all__ = [
    Entity.__name__,
]
