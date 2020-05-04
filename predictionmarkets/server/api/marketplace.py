import json
import typing as t

import grpc  # type: ignore

from ...marketplace import Marketplace, MarketId
from ...markets import CfarMarket
from ...probabilities import Probability

from .protobuf.service_pb2_grpc import MarketplaceServicer  # type: ignore
from .protobuf import service_pb2 as proto  # type: ignore

class MarketplaceServer(MarketplaceServicer):
    def __init__(self, marketplace: Marketplace) -> None:
        self.marketplace = marketplace

    def CreateMarket(self, request: proto.CreateMarketRequest, context: grpc.ServicerContext) -> proto.CreateMarketResponseOrError:
        print('request', request, 'context', context)
        errors: t.MutableMapping[str, t.MutableSequence[str]] = {}
        if not request.name: errors.setdefault("name", []).append("must be non-empty")
        if not request.proposition: errors.setdefault("proposition", []).append("must be non-empty")
        if errors:
            return grpc.Status(grpc.StatusCode.INVALID_ARGUMENT, json.dumps(errors))
        self.marketplace.register_market(CfarMarket(
            name=request.name,
            proposition=request.proposition,
            floor=Probability(ln_odds=request.floor.ln_odds),
            ceiling=Probability(ln_odds=request.ceiling.ln_odds),
            state=Probability(ln_odds=request.initial_state.ln_odds),
        ))
        return proto.CreateMarketResponseOrError(success=proto.CreateMarketResponse())

    def GetMarket(self, request: proto.GetMarketRequest, context: grpc.ServicerContext) -> proto.GetMarketResponseOrError:
        market = self.marketplace.markets.get(MarketId(request.id))
        if market is None:
            return grpc.Status(grpc.StatusCode.NOT_FOUND, "no such market")
        return proto.GetMarketResponseOrError(success=proto.GetMarketResponse(cfar=proto.CfarMarket(
            name=market.name,
            proposition=market.proposition,
            floor=proto.Probability(ln_odds=market.floor.ln_odds),
            ceiling=proto.Probability(ln_odds=market.ceiling.ln_odds),
            state=proto.Probability(ln_odds=market.state.ln_odds),
            entity_stakes={
                e: proto.Stakes(winnings_if_yes=s.if_resolves_yes, winnings_if_no=s.if_resolves_no)
                for e, s in market.stakes.items()
            }
        )))

    def UpdateCfarMarket(self, request: proto.UpdateCfarMarketRequest, context: grpc.ServicerContext) -> proto.UpdateCfarMarketResponseOrError:
        market = self.marketplace.markets.get(MarketId(request.market_id))
        if market is None:
            return grpc.Status(grpc.StatusCode.NOT_FOUND, "no such market")
        market.set_state(participant=request.participant_id, new_state=Probability(ln_odds=request.new_state.ln_odds))
        return proto.UpdateCfarMarketResponseOrError(success=proto.UpdateCfarMarketResponse())
