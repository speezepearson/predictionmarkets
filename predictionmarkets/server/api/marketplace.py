import grpc

from ..marketplace import Marketplace

from ..protobuf.service_pb2_grpc import MarketplaceServicer
import ..protobuf.service_pb2 as proto

class MarketplaceServer(MarketplaceServicer):
    def __init__(self, marketplace: Marketplace) -> None:
        self.marketplace = marketplace

    def CreateMarket(self, request: proto.CreateMarketRequest, context: grpc.ServicerContext) -> proto.CreateMarketResponse:
        errors = {}
        if not request.name: errors.setdefault("name", []).append("must be non-empty")
        if not request.proposition: errors.setdefault("proposition", []).append("must be non-empty")
        if errors:
            return grpc.Status(grpc.StatusCode.INVALID_ARGUMENT, json.dumps(errors))
        self.marketplace.register_market(CfarMarket(
            name=request.name,
            proposition=request.proposition,
            floor=Probability(ln_odds=request.floor.ln_odds),
            ceiling=Probability(ln_odds=request.ceiling.ln_odds),
            state=Probability(ln_odds=request.state.ln_odds),
        ))
        return proto.CreateMarketResponse()

    def GetMarket(self, request: proto.GetMarketRequest, context: grpc.ServicerContext) -> proto.GetMarketResponse:
        market = self.marketplace.markets.get(request.id)
        if market is None:
            return grpc.Status(grpc.StatusCode.NOT_FOUND, "no such market")
        return proto.GetMarketResponse(cfar=proto.CfarMarket(
            name=market.name,
            proposition=market.proposition,
            floor=proto.Probability(ln_odds=market.floor.ln_odds),
            ceiling=proto.Probability(ln_odds=market.ceiling.ln_odds),
            state=proto.Probability(ln_odds=market.state.ln_odds),
            entity_stakes={
                e: proto.Stakes(winnings_if_yes=s.if_resolves_yes, winnings_if_no=s.if_resolves_no)
                for e, s in market.stakes.items()
            }
        ))

    def UpdateCfarMarket(self, request: proto.UpdateCfarMarketRequest, context: grpc.ServicerContext) -> proto.UpdateCfarMarketResponse:
        market = self.marketplace.markets.get(request.market_id)
        if market is None:
            return grpc.Status(grpc.StatusCode.NOT_FOUND, "no such market")
        market.set_state(participant=request.entity_id, new_state=state)
        return proto.UpdateCfarMarketResponse()
