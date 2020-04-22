from __future__ import annotations
import dataclasses
import typing as t

from . import EntityId
from .entity import Entity


@dataclasses.dataclass
class Permission:
    granted_via: t.Optional[Permission]


class PermissionStore:
    def __init__(self):
        self.permissions_by_entity: t.MutableMapping[Entity, t.MutableSet[Permission]] = {}

    def get_permissions(self, entity: Entity) -> t.AbstractSet[Permission]:
        return self.permissions_by_entity.get(entity, set())

    def add_permission(self, entity: Entity, permission: Permission) -> None:
        self.permissions_by_entity.setdefault(entity, set()).add(permission)


__all__ = [
    Permission.__name__,
    PermissionStore.__name__,
]
