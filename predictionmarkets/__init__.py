import dataclasses
import math
import random
import typing as t

from .words import random_words

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

MarketId = t.NewType("MarketId", str)

class Marketplace:
    def __init__(self, rng: t.Optional[random.Random] = None) -> None:
        self.insec_rng = rng if (rng is not None) else random.Random()
        self.markets: t.Dict[MarketId, CfarMarket] = {}

    def register_market(self, market: CfarMarket) -> MarketId:
        id = MarketId('-'.join(random_words(4, rng=self.insec_rng)))
        while id in self.markets:
            id = MarketId('-'.join(random_words(4, rng=self.insec_rng)))
        self.markets[id] = market
        return id
