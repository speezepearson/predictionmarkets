import dataclasses
import math
import typing as t

from plauth import Entity  # type: ignore

from .probabilities import Probability

@dataclasses.dataclass(frozen=True)
class Stakes:
    if_resolves_yes: float
    if_resolves_no: float

@dataclasses.dataclass
class CfarMarket:
    name: str
    proposition: str
    floor: Probability
    ceiling: Probability
    state: Probability
    stakes: t.MutableMapping[Entity, Stakes] = dataclasses.field(default_factory=dict)

    def set_state(self, participant: Entity, new_state: Probability) -> None:
        if not (self.floor <= new_state <= self.ceiling):
            raise ValueError(f"this market's state must be in range [{float(self.floor)}, {float(self.ceiling)}] (got {float(new_state)})")
        stakes = self.stakes.setdefault(participant, Stakes(0, 0))
        p0 = float(self.state)
        p = float(new_state)
        stakes = dataclasses.replace(
            stakes,
            if_resolves_yes=stakes.if_resolves_yes + math.log(p/p0),
            if_resolves_no=stakes.if_resolves_no + math.log((1-p)/(1-p0)),
        )
        self.state, self.stakes[participant] = new_state, stakes

__all__ = [
    CfarMarket.__name__,
    Probability.__name__,
]
