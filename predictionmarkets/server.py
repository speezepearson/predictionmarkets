from __future__ import annotations

import argparse
import collections
import dataclasses
import math
from pathlib import Path
import random
import typing as t

from aiohttp import web
import aiohttp_session  # type: ignore
import plauth  # type: ignore

from . import Probability, CfarMarket, Marketplace, MarketId
from .words import random_words

import jinja2

Username = t.NewType("Username", str)
EntityId = t.NewType("EntityId", str)
Petname = t.NewType("Petname", str)

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

class PetnameRegistry:
    def __init__(self):
        self.viewer_viewed_to_name: t.MutableMapping[t.Tuple[EntityId, EntityId], Petname] = {}

    def add(self, viewer: EntityId, viewed: EntityId, name: Petname) -> None:
        print(f"adding petname {viewer},{viewed} -> {name}")
        self.viewer_viewed_to_name[viewer, viewed] = name
    def get(self, viewer: EntityId, viewed: EntityId) -> t.Optional[Petname]:
        print(f"getting petname for {viewer},{viewed} -> {self.viewer_viewed_to_name.get((viewer, viewed))}")
        return self.viewer_viewed_to_name.get((viewer, viewed))

class MarketResources:
    def __init__(self, router: web.UrlDispatcher) -> None:
        self.index = router.add_resource(name="index", path="/")
        self.market = router.add_resource(name="market", path="/market/{id}")
        self.create_market = router.add_resource(name="create_market", path="/create-market")
        self.user_login = router.add_resource(name="user_login", path="/user_login")
        self.logout = router.add_resource(name="logout", path="/logout")
        self.petname = router.add_resource(name="petname", path="/petname")

    def index_path(self):
        return self.index.url_for()
    def create_market_path(self):
        return self.create_market.url_for()
    def market_path(self, id: MarketId):
        return self.market.url_for(id=id)
    def user_login_path(self):
        return self.user_login.url_for()
    def logout_path(self):
        return self.logout.url_for()
    def petname_path(self):
        return self.petname.url_for()

class Server:
    def __init__(self, marketplace: Marketplace, resources: MarketResources, rng: t.Optional[random.Random] = None) -> None:
        self.marketplace = marketplace
        self.resources = resources
        self.rng = rng if (rng is not None) else random.Random()
        self.jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader("predictionmarkets", "templates"),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        self.bcrypt_entities: t.MutableMapping[EntityId, plauth.AnybodyWithThisBcryptInverse] = {}
        self.username_to_entity_id: t.MutableMapping[Username, EntityId] = collections.defaultdict(lambda: EntityId("-".join(random_words(4, rng=self.rng))))
        self.petnames: PetnameRegistry = PetnameRegistry()

        self.jinja_env.globals["resources"] = self.resources
        self.jinja_env.globals["petnames"] = self.petnames

    def add_handlers(self):
        self.resources.index.add_route("GET", self.get_index)
        self.resources.create_market.add_route(method="GET", handler=self.get_create_market)
        self.resources.create_market.add_route(method="POST", handler=self.post_create_market)
        self.resources.market.add_route(method="GET", handler=self.get_market),
        self.resources.market.add_route(method="POST", handler=self.post_market),
        self.resources.user_login.add_route(method="POST", handler=self.post_user_login),
        self.resources.logout.add_route(method="POST", handler=self.post_logout),
        self.resources.petname.add_route(method="POST", handler=self.post_petname),


    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("index.jinja.html").render(
                public_markets=self.marketplace.markets,
                current_entity=session.entity_id,
                current_path=request.path,
            ),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("create-market.jinja.html").render(
                current_entity=session.entity_id,
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
                current_entity=session.entity_id,
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

    async def post_user_login(self, request: web.Request) -> web.StreamResponse:
        # TODO: actual auth
        session = Session(await aiohttp_session.get_session(request))

        post_data = await request.post()
        try:
            username = Username(str(post_data["username"]))
            password = Username(str(post_data["password"]))
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))

        entity_id = self.username_to_entity_id[username]
        if entity_id not in self.bcrypt_entities:
            self.bcrypt_entities[entity_id] = plauth.AnybodyWithThisBcryptInverse.from_password(password)

        if self.bcrypt_entities[entity_id].check_password(password).accepted:
            session.entity_id = entity_id
            return web.Response(
                status=200,
                body=self.jinja_env.get_template("redirect.jinja.html").render(text="Logged in!", dest=redirect_to),
                content_type="text/html",
            )

        return web.HTTPUnauthorized()

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

    async def post_petname(self, request: web.Request) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        if session.entity_id is None:
            return web.HTTPUnauthorized()

        post_data = await request.post()
        try:
            entity_id = EntityId(str(post_data["entityId"]))
            petname = Petname(str(post_data["petname"]))
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))

        self.petnames.add(session.entity_id, entity_id, petname)

        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(text="Added petname!", dest=redirect_to),
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
