import dataclasses
import math

@dataclasses.dataclass(order=True)
class Probability:
    ln_odds: float

    def __float__(self):
        odds = math.exp(self.ln_odds)
        return odds/(odds+1)
