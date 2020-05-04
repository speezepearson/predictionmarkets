import json
import typing as t

from .entity import EntityId

Petname = t.NewType("Petname", str)

class PetnameService:
    def __init__(self):
        self.viewer_to_viewed_to_name: t.MutableMapping[t.EntityId, t.MutableMapping[EntityId, Petname]] = {}

    def add_petname(self, viewer: EntityId, viewed: EntityId, name: Petname) -> None:
        self.viewer_to_viewed_to_name.setdefault(viewer, {})[viewed] = name

    def get_petnames(self, viewer: EntityId) -> t.Mapping[EntityId, Petname]:
        return self.viewer_to_viewed_to_name.get(viewer, {})

    def get_petname(self, viewer: EntityId, viewed: EntityId) -> t.Optional[Petname]:
        return self.viewer_to_viewed_to_name.get(viewer, {}).get(viewed)
