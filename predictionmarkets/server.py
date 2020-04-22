import argparse
import dataclasses
import math
from pathlib import Path
import random
import typing as t

from aiohttp import web
import aiohttp_session  # type: ignore

from . import Probability, CfarMarket, Marketplace, MarketId
from .auth import EntityId

import jinja2

class MarketResources:
    def __init__(self, router: web.UrlDispatcher) -> None:
        self.index = router.add_resource(name="index", path="/")
        self.market = router.add_resource(name="market", path="/market/{id}")
        self.create_market = router.add_resource(name="create_market", path="/create-market")
        self.login = router.add_resource(name="login", path="/login")

    def index_path(self):
        return self.index.url_for()
    def create_market_path(self):
        return self.create_market.url_for()
    def market_path(self, id: MarketId):
        return self.market.url_for(id=id)
    def login_path(self):
        return self.login.url_for()

class Server:
    def __init__(self, marketplace: Marketplace, resources: MarketResources) -> None:
        self.marketplace = marketplace
        self.resources = resources
        self.jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader("predictionmarkets", "templates"),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        self.jinja_env.globals["resources"] = self.resources

    def add_handlers(self):
        self.resources.index.add_route("GET", self.get_index)
        self.resources.create_market.add_route(method="GET", handler=self.get_create_market)
        self.resources.create_market.add_route(method="POST", handler=self.post_create_market)
        self.resources.market.add_route(method="GET", handler=self.get_market),
        self.resources.market.add_route(method="POST", handler=self.post_market),
        self.resources.login.add_route(method="POST", handler=self.post_login),


    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        session = await aiohttp_session.get_session(request)
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("index.jinja.html").render(
                public_markets=self.marketplace.markets,
                logged_in_user=session.get("username"),
            ),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("create-market.jinja.html").render(),
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
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Market created!", dest=self.resources.market_path(id=id)),
            content_type="text/html",
        )

    async def get_market(self, request: web.Request) -> web.StreamResponse:
        id = MarketId(str(request.match_info["id"]))
        market = self.marketplace.markets.get(id)
        if market is None:
            return web.HTTPNotFound()
        session = await aiohttp_session.get_session(request)
        return web.Response(
            status=200,
            body=self.jinja_env.get_template('view-market.jinja.html').render(
                id=id,
                market=market,
                logged_in_user=session.get("username"),
            ),
            content_type="text/html",
        )

    async def post_market(self, request: web.Request) -> web.StreamResponse:
        market_id = MarketId(str(request.match_info["id"]))
        market = self.marketplace.markets.get(market_id)
        if market is None:
            return web.HTTPNotFound()

        session = await aiohttp_session.get_session(request)
        entity_id = EntityId(session["username"])

        post_data = await request.post()
        try:
            state = Probability(ln_odds=float(str(post_data["state"])))
        except (KeyError, ValueError) as e:
            return web.HTTPBadRequest(reason=str(e))
        market.set_state(participant=entity_id, new_state=state)
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Market updated!", dest=self.resources.market_path(id=market_id)),
            content_type="text/html",
        )

    async def post_login(self, request: web.Request) -> web.StreamResponse:
        # TODO: actual auth
        post_data = await request.post()
        session = await aiohttp_session.get_session(request)
        session["username"] = str(post_data["username"]) # TODO: handle KeyError
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Logged in!", dest=self.resources.index_path()),
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
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
    Server(marketplace, MarketResources(app.router)).add_handlers()

    web.run_app(app, host=args.host, port=args.port)
