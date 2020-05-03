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

import .protobuf.service_pb2 as proto
from . import Probability, CfarMarket, Marketplace, MarketId
from .words import random_words
from .api.markets import MarketplaceServer
from .api.entity import EntityServer, Token

import jinja2

Petname = t.NewType("Petname", str)

class Session:
    _TOKEN_KEY = "token"

    def __init__(self, aio_session: aiohttp_session.Session) -> None:
        self._aio_session = aio_session

    @property
    def token(self) -> t.Optional[Token]:
        # TODO: should use session.identity instead, and have a separate map to translate to entity-id
        s = self._aio_session.get(Session._TOKEN_KEY)
        if s is None:
            return None
        return Token(s)
    @token.setter
    def token(self, value: t.Optional[Token]) -> None:
        if value is None:
            del self._aio_session[Session._TOKEN_KEY]
        else:
            self._aio_session[Session._TOKEN_KEY] = value

class PetnameRegistry:
    def __init__(self):
        self.viewer_viewed_to_name: t.MutableMapping[t.Tuple[EntityId, EntityId], Petname] = {}

    def add(self, viewer: EntityId, viewed: EntityId, name: Petname) -> None:
        self.viewer_viewed_to_name[viewer, viewed] = name
    def get(self, viewer: EntityId, viewed: EntityId) -> t.Optional[Petname]:
        return self.viewer_viewed_to_name.get((viewer, viewed))

class MarketResources:
    def __init__(self, router: web.UrlDispatcher) -> None:
        self.index = router.add_resource(name="index", path="/")
        self.market = router.add_resource(name="market", path="/market/{id}")
        self.create_market = router.add_resource(name="create_market", path="/create-market")
        self.user_login = router.add_resource(name="user_login", path="/user_login")
        self.logout = router.add_resource(name="logout", path="/logout")
        self.petname = router.add_resource(name="petname", path="/petname")
        self.entity = router.add_resource(name="entity", path="/entity/{id}")

    def index_path(self):  # TODO: return type annotation
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
    def entity_path(self, id: EntityId):
        return self.entity.url_for(id=id)

class Server:
    def __init__(
        self,
        entity_service: proto.EntityServicer,
        market_service: proto.MarketplaceServicer,
        resources: MarketResources,
    ) -> None:
        self.entity_service = entity_service
        self.market_service = market_service
        self.resources = resources
        self.jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader("predictionmarkets", "templates"),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            # TODO: undefined=StrictUndefined or something like that
        )
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
        self.resources.entity.add_route(method="GET", handler=self.get_entity),

    def _get_entity(session: Session) -> t.Optional[EntityId]:
        response = self.entity_service.GetEntityForToken(
            request=proto.GetEntityForTokenRequest(token=session.token),
            context=None,
        )  # TODO: error-handling
        return response.entity_id

    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("index.jinja.html").render(
                public_markets=self.marketplace.markets,
                current_entity=current_entity,
                current_path=request.path,
            ),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("create-market.jinja.html").render(
                current_entity=current_entity,
                current_path=request.path,
            ),
            content_type="text/html",
        )

    async def post_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        response = self.market_service.CreateMarket(
            request=proto.CreateMarketRequest(
                name=str(post_data["name"]),
                proposition=str(post_data["proposition"]),
                floor=proto.Probability(ln_odds=float(str(post_data["floor"]))),
                ceiling=proto.Probability(ln_odds=float(str(post_data["ceiling"]))),
                state=proto.Probability(ln_odds=float(str(post_data["state"]))),
            ),
            context=None
        )  # TODO: error-handling
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(
                text="Market created!",
                dest=self.resources.market_path(id=response.market_id),
            ),
            content_type="text/html",
        )

    async def get_market(self, request: web.Request) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        response = self.market_service.GetMarket(
            request=proto.GetMarketRequest(id=str(request.match_info["id"])),
            context=None
        )  # TODO: error-handling
        return web.Response(
            status=200,
            body=self.jinja_env.get_template('view-market.jinja.html').render(
                id=id,
                market=response.cfar,  # TODO: deal with polymorphism
                current_entity=current_entity,  # TODO: these two arguments get passed in a lot; can we refactor them out?
                current_path=request.path,
            ),
            content_type="text/html",
        )

    async def post_market(self, request: web.Request) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        post_data = await request.post()
        market_id = MarketId(str(request.match_info["id"]))
        response = self.market_service.UpdateCfarMarket(
            request=proto.UpdateCfarMarketRequest(
                market_id=market_id,
                entity_id=current_entity,
                new_state=proto.Probability(ln_odds=str(post_data["state"])),
            ),
            context=None,
        )  # TODO: error-handling
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(
                text="Market updated!",
                dest=self.resources.market_path(id=market_id),
            ),
            content_type="text/html",
        )

    async def post_user_login(self, request: web.Request) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        if session.token is not None:
            raise NotImplementedError()  # TODO

        post_data = await request.post()
        try:
            username = Username(str(post_data["username"]))
            password = str(post_data["password"])
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))
        response = self.entity_service.UsernamePasswordLogin(
            request=proto.UsernamePasswordLoginRequest(
                username=username,
                password=password,
            ),
            context=None,
        )  # TODO: error-handling
        session.token = response.token

        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(
                text="Logged in!",
                dest=redirect_to,
            ),
            content_type="text/html",
        )

    async def post_logout(self, request: web.Request) -> web.StreamResponse:
        session = Session(await aiohttp_session.get_session(request))
        response = self.entity_service.DeleteToken(
            request=proto.DeleteTokenRequest(token=session.token),
            context=None,
        )  # TODO: error-handling

        session.token = None

        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(
                text="Logged out!",
                dest=redirect_to,
            ),
            content_type="text/html",
        )

    async def post_petname(self, request: web.Request) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        if current_entity is None:
            return web.HTTPUnauthorized()

        post_data = await request.post()
        try:
            entity_id = EntityId(str(post_data["entityId"]))
            petname = Petname(str(post_data["petname"]))
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))

        self.petnames.add(current_entity, entity_id, petname)

        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(
                text="Added petname!",
                dest=redirect_to,
            ),
            content_type="text/html",
        )

    async def get_entity(self, request: web.Request) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        id = request.match_info["id"]
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("view-entity.jinja.html").render(
                id=id,
                current_entity=current_entity,
                current_path=request.path,
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
    marketplace = Marketplace(rng=rng)

    app = web.Application()
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
    Server(marketplace, MarketResources(app.router)).add_handlers()

    web.run_app(app, host=args.host, port=args.port)
