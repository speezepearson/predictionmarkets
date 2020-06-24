from pathlib import Path

from aiohttp import web

from ....markets import CfarMarket
from ....marketplace import Marketplace
from ....probabilities import Probability
from ...api import marketplace
from ...api.protobuf.predictionmarkets import marketplace_pb2

m = Marketplace()
for n in range(23):
    m.register_market(CfarMarket(
        name=f'name {n}',
        proposition=f'details {n}',
        floor=Probability(ln_odds=-10),
        ceiling=Probability(ln_odds=10),
        state=Probability(ln_odds=n/100),
    ))

routes = web.RouteTableDef()

@routes.get('/')
async def index(req):
    return web.FileResponse(Path(__file__).parent.parent/'elm'/'dist'/'MarketList.html')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    app.add_routes(marketplace.make_routes(m))
    web.run_app(app, host='localhost', port=8080)
