from typing import Callable, Type, TypeVar, Awaitable
from aiohttp import web
from google.protobuf.message import Message

Req = TypeVar('Req', bound=Message)
Resp = TypeVar('Resp', bound=Message)

def protobuf(
    req_type: Type[Req],
    resp_type: Type[Resp],
) -> Callable[
    [Callable[[web.BaseRequest, Req], Awaitable[Resp]]],
    Callable[[web.BaseRequest], Awaitable[web.StreamResponse]]
]:
    def wrap(endpoint: Callable[[web.BaseRequest, Req], Awaitable[Resp]]) -> Callable[[web.BaseRequest], Awaitable[web.StreamResponse]]:
        async def wrapped(request: web.BaseRequest) -> web.StreamResponse:
            request_pb = req_type.FromString(await request.content.read())
            response_pb = await endpoint(request, request_pb)
            return web.Response(
                status=200,
                content_type="application/octet-stream",
                body=response_pb.SerializeToString(),
            )
        return wrapped
    return wrap
