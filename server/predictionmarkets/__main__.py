import argparse
import dataclasses
import math
from pathlib import Path
import typing as t
from aiohttp import web

import pystache  # type: ignore

from predictionmarkets.util import random_words

MarketId = t.NewType("MarketId", str)

TEMPLATE_DIR = Path(__file__).parent / "templates"


@dataclasses.dataclass
class Probability:
    ln_odds: float

    def __float__(self):
        odds = math.exp(self.ln_odds)
        return odds/(odds+1)


@dataclasses.dataclass
class CfarMarket:
    name: str
    proposition: str
    floor: Probability
    ceiling: Probability
    state: Probability


def render_market(market: CfarMarket) -> str:
    return pystache.render(
        template=(TEMPLATE_DIR/'market.mustache.html').read_text(),
        context=dataclasses.asdict(market),
    )


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
            body=pystache.render(
                template=(TEMPLATE_DIR/"index.mustache.html").read_text(),
                context={
                    "markets": [
                        {"id": id, **dataclasses.asdict(market)}
                        for id, market in self.markets.items()
                    ],
                },
            ),
            content_type="text/html",
        )

    async def create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        id = MarketId(random_words(4))
        post_data = await request.post()
        market = CfarMarket(
            name=str(post_data["name"]),
            proposition=str(post_data["proposition"]),
            floor=Probability(ln_odds=float(str(post_data["floor"]))),
            ceiling=Probability(ln_odds=float(str(post_data["ceiling"]))),
            state=Probability(ln_odds=float(str(post_data["state"]))),
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
