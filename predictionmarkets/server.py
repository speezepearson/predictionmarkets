import argparse
import dataclasses
import math
from pathlib import Path
import random
import typing as t
from aiohttp import web

from . import Probability, CfarMarket, Marketplace, MarketId

import jinja2

jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader('predictionmarkets', 'templates'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

class Server:
    def __init__(self, marketplace: Marketplace) -> None:
        self.marketplace = marketplace

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
            body=jinja_env.get_template("index.jinja.html").render(public_markets=self.marketplace.markets),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.Response(
            status=200,
            body=jinja_env.get_template("create-market.jinja.html").render(),
            content_type="text/html",
        )

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

        id = self.marketplace.register_market(market)
        return web.Response(
            status=200,
            body=jinja_env.get_template("redirect.jinja.html").render(text="Market created!", dest=f"/market/{id}"),
            content_type="text/html",
        )

    async def get_market(self, request: web.Request) -> web.StreamResponse:
        id = MarketId(str(request.match_info["id"]))
        market = self.marketplace.markets.get(id)
        if market is None:
            return web.Response(status=404)
        return web.Response(
            status=200,
            body=jinja_env.get_template('view-market.jinja.html').render(id=id, market=market),
            content_type="text/html",
        )

    async def update_market(self, request: web.Request) -> web.StreamResponse:
        id = MarketId(str(request.match_info["id"]))
        market = self.marketplace.markets.get(id)
        if market is None:
            return web.Response(status=404)

        try:
            state = Probability(ln_odds=float(str((await request.post())["state"])))
        except (KeyError, ValueError) as e:
            return web.HTTPBadRequest(reason=str(e))
        market.state = state
        return web.Response(
            status=200,
            body=jinja_env.get_template("redirect.jinja.html").render(text="Market updated!", dest=f"/market/{id}"),
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
    marketplace = Marketplace(rng=rng)

    app = web.Application()
    app.add_routes(Server(marketplace).routes())

    web.run_app(app, host=args.host, port=args.port)
