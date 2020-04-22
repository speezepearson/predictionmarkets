from __future__ import annotations
import bcrypt
import hashlib
import dataclasses
import typing as t

from .authenticator import Authenticator

EntityId = t.NewType("EntityId", str)

@dataclasses.dataclass(frozen=True)
class Entity:
    id: EntityId
    authenticator: Authenticator

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return f"<Entity {self.id}>"

__all__ = [
    EntityId.__name__,
    Entity.__name__,
]
