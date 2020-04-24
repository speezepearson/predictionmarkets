from __future__ import annotations

import argparse
import dataclasses
import math
from pathlib import Path
import random
import typing as t

from aiohttp import web
import aiohttp_session  # type: ignore

from . import Probability, CfarMarket, Marketplace, MarketId

import jinja2

EntityId = t.NewType("EntityId", str)

class Session:
    _ENTITY_ID_KEY = "entity_id"

    def __init__(self, aio_session: aiohttp_session.Session) -> None:
        self._aio_session = aio_session

    @property
    def entity_id(self) -> t.Optional[EntityId]:
        s = self._aio_session.get(Session._ENTITY_ID_KEY)
        if s is None:
            return None
        return EntityId(s)
    @entity_id.setter
    def entity_id(self, value: t.Optional[EntityId]) -> None:
        if value is None:
            del self._aio_session[Session._ENTITY_ID_KEY]
        else:
            self._aio_session[Session._ENTITY_ID_KEY] = value

class MarketResources:
    def __init__(self, router: web.UrlDispatcher) -> None:
        self.index = router.add_resource(name="index", path="/")
        self.market = router.add_resource(name="market", path="/market/{id}")
        self.create_market = router.add_resource(name="create_market", path="/create-market")
        self.login = router.add_resource(name="login", path="/login")
        self.logout = router.add_resource(name="logout", path="/logout")

    def index_path(self):
        return self.index.url_for()
    def create_market_path(self):
        return self.create_market.url_for()
    def market_path(self, id: MarketId):
        return self.market.url_for(id=id)
    def login_path(self):
        return self.login.url_for()
    def logout_path(self):
        return self.logout.url_for()

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
        self.resources.logout.add_route(method="POST", handler=self.post_logout),


    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("index.jinja.html").render(
                public_markets=self.marketplace.markets,
                logged_in_user=session.entity_id,
                current_path=request.path,
            ),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("create-market.jinja.html").render(
                logged_in_user=session.entity_id,
                current_path=request.path,
            ),
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
        session = Session(await aiohttp_session.get_session(request))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template('view-market.jinja.html').render(
                id=id,
                market=market,
                logged_in_user=session.entity_id,
                current_path=request.path,
            ),
            content_type="text/html",
        )

    async def post_market(self, request: web.Request) -> web.StreamResponse:
        market_id = MarketId(str(request.match_info["id"]))
        market = self.marketplace.markets.get(market_id)
        if market is None:
            return web.HTTPNotFound()

        session = Session(await aiohttp_session.get_session(request))
        if session.entity_id is None:
            return web.HTTPUnauthorized(reason="You gotta log in!")

        post_data = await request.post()
        try:
            state = Probability(ln_odds=float(str(post_data["state"])))
        except (KeyError, ValueError) as e:
            return web.HTTPBadRequest(reason=str(e))
        market.set_state(participant=session.entity_id, new_state=state)
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Market updated!", dest=self.resources.market_path(id=market_id)),
            content_type="text/html",
        )

    async def post_login(self, request: web.Request) -> web.StreamResponse:
        # TODO: actual auth
        session = Session(await aiohttp_session.get_session(request))

        post_data = await request.post()
        try:
            session.entity_id = EntityId(str(post_data["username"]))
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))

        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Logged in!", dest=redirect_to),
            content_type="text/html",
        )

    async def post_logout(self, request: web.Request) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        session.entity_id = None
        post_data = await request.post()
        try:
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))

        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Logged out!", dest=redirect_to),
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
