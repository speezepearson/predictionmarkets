import random
import typing as t

from .markets import CfarMarket
from .words import random_words

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
