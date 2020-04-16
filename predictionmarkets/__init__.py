import dataclasses
import math

@dataclasses.dataclass
class Probability:
    ln_odds: float

    def __float__(self):
        odds = math.exp(self.ln_odds)
        return odds/(odds+1)


@dataclasses.dataclass
class CfarMarket:
    name: str
    proposition: str
    floor: Probability
    ceiling: Probability
    state: Probability
