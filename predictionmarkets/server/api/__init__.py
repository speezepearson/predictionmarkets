import argparse
from pathlib import Path

from aiohttp import web

from . import pb_decorator
from .protobuf.predictionmarkets import marketplace_pb2, auth_pb2

def make_routes(
    list_markets_func,
    username_log_in_func,
    log_out_func,
) -> web.RouteTableDef:
    # TODO: fix this crummy signature

    routes = web.RouteTableDef()

    @routes.post('/api/v1/list_markets')
    @pb_decorator.protobuf(marketplace_pb2.ListMarketsRequest, marketplace_pb2.ListMarketsResponse)
    async def list_markets(
        request: web.BaseRequest,
        request_pb: marketplace_pb2.ListMarketsRequest
    ) -> marketplace_pb2.ListMarketsResponse:
        return marketplace_pb2.ListMarketsResponse(market_infos=list_markets_func(limit=request_pb.limit, offset=request_pb.offset))

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
