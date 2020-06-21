from pathlib import Path

from aiohttp import web

from .. import api
from ..api.protobuf.predictionmarkets import marketplace_pb2

markets = {
    n: marketplace_pb2.MarketInfo(name=f"name {n}", details=f"details {n}")
    for n in range(33)
}

routes = web.RouteTableDef()

@routes.get('/')
async def index(req):
    return web.FileResponse(Path(__file__).parent/'elm'/'dist'/'MarketList.html')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    app.add_routes(api.make_routes(lambda limit, offset: {
        str(n): markets[n]
        for n in range(offset, offset+limit)
        if n in markets
    }))
    web.run_app(app, host='localhost', port=8080)
