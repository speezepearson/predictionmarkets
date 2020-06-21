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

    @routes.post('/api/v1/username_log_in')
    @pb_decorator.protobuf(auth_pb2.UsernameLogInRequest, auth_pb2.UsernameLogInResponse)
    async def username_log_in(
        request: web.BaseRequest,
        request_pb: auth_pb2.UsernameLogInRequest
    ) -> auth_pb2.UsernameLogInResponse:
        return auth_pb2.UsernameLogInResponse(entity_id=username_log_in_func(username=request_pb.username, password=request_pb.password))

    @routes.post('/api/v1/log_out')
    @pb_decorator.protobuf(auth_pb2.LogOutRequest, auth_pb2.LogOutResponse)
    async def log_out(
        request: web.BaseRequest,
        request_pb: auth_pb2.LogOutRequest
    ) -> auth_pb2.LogOutResponse:
        return auth_pb2.LogOutResponse()

    return routes
