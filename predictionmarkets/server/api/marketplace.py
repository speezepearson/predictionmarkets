import argparse
from pathlib import Path

from aiohttp import web

from predictionmarkets.marketplace import Marketplace
from . import pb_decorator
from .protobuf.predictionmarkets import marketplace_pb2

def make_routes(
    marketplace: Marketplace,
) -> web.RouteTableDef:
    # TODO: fix this crummy signature

    routes = web.RouteTableDef()

    @routes.post('/api/v1/list_markets')
    @pb_decorator.protobuf(marketplace_pb2.ListMarketsRequest, marketplace_pb2.ListMarketsResponse)
    async def list_markets(
        request: web.BaseRequest,
        request_pb: marketplace_pb2.ListMarketsRequest
    ) -> marketplace_pb2.ListMarketsResponse:
        return marketplace_pb2.ListMarketsResponse(market_infos={
            id: marketplace_pb2.MarketInfo(name=market.name, details=market.proposition)
            for id, market in marketplace.get_public_markets().items()
        })

    return routes
