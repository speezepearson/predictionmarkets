import argparse
from pathlib import Path

from aiohttp import web

from . import pb_decorator
from .protobuf.predictionmarkets import marketplace_pb2

def make_routes(list_markets_func) -> web.RouteTableDef:
    # TODO: fix this crummy signature

    routes = web.RouteTableDef()

    @routes.post('/api/v1/list_markets')
    @pb_decorator.protobuf(marketplace_pb2.ListMarketsRequest, marketplace_pb2.ListMarketsResponse)
    async def list_markets(
        request: web.BaseRequest,
        request_pb: marketplace_pb2.ListMarketsRequest
    ) -> marketplace_pb2.ListMarketsResponse:
        return marketplace_pb2.ListMarketsResponse(market_infos=list_markets_func(limit=request_pb.limit, offset=request_pb.offset))

    return routes
