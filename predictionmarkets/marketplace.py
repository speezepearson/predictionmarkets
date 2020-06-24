import random
import typing as t

from plauth.authenticator import EntityId

from .markets import CfarMarket, Probability
from .words import random_words

MarketId = t.NewType("MarketId", str)

class Marketplace:
    def __init__(self, rng: t.Optional[random.Random] = None) -> None:
        self.insec_rng = rng if (rng is not None) else random.Random()
        self.markets: t.MutableMapping[MarketId, CfarMarket] = {}

    def get_public_markets(self) -> t.Mapping[MarketId, CfarMarket]:
        return self.markets

    def register_market(self, market: CfarMarket) -> MarketId:
        id = MarketId('-'.join(random_words(4, rng=self.insec_rng)))
        while id in self.markets:
            id = MarketId('-'.join(random_words(4, rng=self.insec_rng)))
        self.markets[id] = market
        return id

    def get_market(self, market_id: MarketId) -> CfarMarket:
        return self.markets[market_id]

    def update_market(self, market_id: MarketId, participant_id: EntityId, new_state: Probability) -> None:
        market = self.markets.get(market_id)
        if market is None:
            raise KeyError(market_id)
        market.set_state(participant=participant_id, new_state=new_state)
