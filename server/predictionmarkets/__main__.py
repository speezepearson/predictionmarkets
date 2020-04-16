import argparse
import dataclasses
import typing as t
from aiohttp import web

from predictionmarkets.util import random_words

MarketId = t.NewType("MarketId", str)


@dataclasses.dataclass
class Probability:
    log_odds: float


@dataclasses.dataclass
class CfarMarket:
    name: str
    proposition: str
    floor: Probability
    ceiling: Probability
    state: Probability


def render_market(market: CfarMarket) -> str:
    return str(market)


class Server:
    def __init__(self) -> None:
        self.markets: t.Dict[MarketId, CfarMarket] = {}

    def routes(self) -> t.Iterable[web.RouteDef]:
        return [
            web.RouteDef(method="GET", path="/", handler=self.get_index, kwargs={}),
            web.RouteDef(method="POST", path="/create-market", handler=self.create_market, kwargs={}),
            web.RouteDef(
                method="GET", path="/market/{id}", handler=self.get_market, kwargs={}
            ),
        ]

    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.Response(
            status=200,
            body="""
                <ul>{}</ul>
                <h1>New Market</h1>
                <form action="/create-market" method="post">
                    <div>Name: <input type="text" name="name"></div>
                    <div>Proposition: <input type="text" name="proposition"></div>
                    <div>Floor: <input type="text" name="floor"></div>
                    <div>Ceiling: <input type="text" name="ceiling"></div>
                    <div>State: <input type="text" name="state"></div>
                    <div><input type="submit" value="Submit"></div>
                </form>
            """.format(
                "".join(
                    f'<li><a href="{id}">{market.name}</a></li>'
                    for id, market in self.markets.items()
                ),

            ),
            content_type='text/html',
        )

    async def create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        id = MarketId(random_words(4))
        post_data = await request.post()
        market = CfarMarket(
            name=str(post_data["name"]),
            proposition=str(post_data["proposition"]),
            floor=Probability(log_odds=float(str(post_data["floor"]))),
            ceiling=Probability(log_odds=float(str(post_data["ceiling"]))),
            state=Probability(log_odds=float(str(post_data["state"]))),
        )
        self.markets[id] = market
        return web.Response(
            status=200,
            body=render_market(market),
            content_type="text/html",
        )

    async def get_market(self, request: web.Request) -> web.StreamResponse:
        id = MarketId(str(request.match_info["id"]))
        market = self.markets.get(id)
        if market is None:
            return web.Response(status=404)
        return web.Response(
            status=200,
            body=render_market(market),
            content_type="text/html",
        )


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=8080)
parser.add_argument("-H", "--host", default="localhost")

if __name__ == "__main__":
    args = parser.parse_args()

    app = web.Application()
    app.add_routes(Server().routes())

    web.run_app(app, host=args.host, port=args.port)
