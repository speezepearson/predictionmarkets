import json
import typing as t

from .authenticator import EntityId

from ...marketplace import Marketplace, MarketId
from ...markets import CfarMarket
from ...probabilities import Probability

class MarketplaceService:
    def __init__(self, marketplace: Marketplace) -> None:
        self.marketplace = marketplace

    def get_public_markets(self) -> t.Mapping[MarketId, CfarMarket]:
        return self.marketplace.markets

    def create_market(self, market: CfarMarket) -> MarketId:
        errors: t.MutableMapping[str, t.MutableSequence[str]] = {}
        if not market.name: errors.setdefault("name", []).append("must be non-empty")
        if not market.proposition: errors.setdefault("proposition", []).append("must be non-empty")
        if errors:
            raise ValueError(errors)
        return self.marketplace.register_market(market)

    def get_market(self, market_id: MarketId) -> CfarMarket:
        return self.marketplace.markets[market_id]

    def update_cfar_market(self, market_id: MarketId, participant_id: EntityId, new_state: Probability) -> None:
        market = self.marketplace.markets.get(market_id)
        if market is None:
            raise KeyError(market_id)
        market.set_state(participant=participant_id, new_state=new_state)
