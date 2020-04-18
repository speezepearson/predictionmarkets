import argparse
import dataclasses
import math
from pathlib import Path
import random
import typing as t
from aiohttp import web

import pystache  # type: ignore

from . import Probability, CfarMarket
from . import words

MarketId = t.NewType("MarketId", str)

TEMPLATE_DIR = Path(__file__).parent / "templates"
INDEX_PAGE_TEMPLATE = TEMPLATE_DIR / "index.mustache.html"
MARKET_PAGE_TEMPLATE = TEMPLATE_DIR / "market.mustache.html"
REDIRECT_TO_MARKET_PAGE_TEMPLATE = TEMPLATE_DIR / "redirect-to-market.mustache.html"
CREATE_MARKET_PAGE_TEMPLATE = TEMPLATE_DIR / "create-market.mustache.html"


class Server:
    def __init__(self, rng: t.Optional[random.Random] = None) -> None:
        self.insec_rng = rng if (rng is not None) else random.Random()
        self.markets: t.Dict[MarketId, CfarMarket] = {}

    def routes(self) -> t.Iterable[web.RouteDef]:
        return [
            web.RouteDef(method="GET", path="/", handler=self.get_index, kwargs={}),
            web.RouteDef(method="GET", path="/create-market", handler=self.get_create_market, kwargs={}),
            web.RouteDef(method="POST", path="/create-market", handler=self.post_create_market, kwargs={}),
            web.RouteDef(method="GET", path="/market/{id}", handler=self.get_market, kwargs={}),
            web.RouteDef(method="POST", path="/market/{id}/update", handler=self.update_market, kwargs={}),
        ]

    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.Response(
            status=200,
            body=pystache.render(
                template=INDEX_PAGE_TEMPLATE.read_text(),
                context={
                    "public_markets": [
                        {"id": id, **dataclasses.asdict(market)}
                        for id, market in self.markets.items()
                    ],
                },
            ),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.Response(
            status=200,
            body=CREATE_MARKET_PAGE_TEMPLATE.read_text(),
            content_type="text/html",
        )

    def register_market(self, market: CfarMarket) -> MarketId:
        id = MarketId('-'.join(words.random_words(4, rng=self.insec_rng)))
        while id in self.markets:
            id = MarketId('-'.join(words.random_words(4, rng=self.insec_rng)))
        self.markets[id] = market
        return id

    async def post_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        post_data = await request.post()
        try:
            market = CfarMarket(
                name=str(post_data["name"]),
                proposition=str(post_data["proposition"]),
                floor=Probability(ln_odds=float(str(post_data["floor"]))),
                ceiling=Probability(ln_odds=float(str(post_data["ceiling"]))),
                state=Probability(ln_odds=float(str(post_data["state"]))),
            )
        except (KeyError, ValueError) as e:
            return web.HTTPBadRequest(reason=str(e))

        id = self.register_market(market)
        return web.Response(
            status=200,
            body=pystache.render(
                template=REDIRECT_TO_MARKET_PAGE_TEMPLATE.read_text(),
                context={"id": id, "text": "Market created!"},
            ),
            content_type="text/html",
        )

    async def get_market(self, request: web.Request) -> web.StreamResponse:
        id = MarketId(str(request.match_info["id"]))
        market = self.markets.get(id)
        if market is None:
            return web.Response(status=404)
        return web.Response(
            status=200,
            body=pystache.render(
                template=MARKET_PAGE_TEMPLATE.read_text(),
                context={"id": id, **dataclasses.asdict(market)},
            ),
            content_type="text/html",
        )

    async def update_market(self, request: web.Request) -> web.StreamResponse:
        id = MarketId(str(request.match_info["id"]))
        market = self.markets.get(id)
        if market is None:
            return web.Response(status=404)

        try:
            state = Probability(ln_odds=float(str((await request.post())["state"])))
        except (KeyError, ValueError) as e:
            return web.HTTPBadRequest(reason=str(e))
        market.state = state
        return web.Response(
            status=200,
            body=pystache.render(
                template=REDIRECT_TO_MARKET_PAGE_TEMPLATE.read_text(),
                context={"id": id, "text": "Market updated!"},
            ),
            content_type="text/html",
        )


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=8080)
parser.add_argument("-H", "--host", default="localhost")
parser.add_argument("--random-seed", type=int, default=None)

if __name__ == "__main__":
    args = parser.parse_args()

    rng = random.Random()
    if args.random_seed is not None:
        rng.seed(args.random_seed)

    app = web.Application()
    app.add_routes(Server(rng=rng).routes())

    web.run_app(app, host=args.host, port=args.port)
