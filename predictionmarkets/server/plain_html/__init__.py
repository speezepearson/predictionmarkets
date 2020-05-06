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
from plauth.authenticator import (
    TokenAuthenticator,
    UsernamePasswordAuthenticator,
    Token,
    Username,
    Password,
    EntityId,
)

from ... import Probability, CfarMarket, Marketplace, MarketId
from ...words import random_words
from ...petnames import Petname, PetnameRegistry

import jinja2


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

class Resources:
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
        token_auth: TokenAuthenticator,
        username_password_auth: UsernamePasswordAuthenticator,
        marketplace: Marketplace,
        petname_registry: PetnameRegistry,
        resources: Resources,
    ) -> None:
        self.token_auth = token_auth
        self.username_password_auth = username_password_auth
        self.marketplace = marketplace
        self.petname_registry = petname_registry
        self.resources = resources
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            # TODO: undefined=StrictUndefined or something like that
        )

        self.jinja_env.globals["resources"] = self.resources

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

    def _get_entity(self, session: Session) -> t.Optional[EntityId]:
        if session.token is None:
            return None
        try:
            return self.token_auth.get_entity_for_token(session.token)
        except KeyError:
            session.token = None
            return None

    def _render_kwargs(self, request: web.BaseRequest, current_entity: t.Optional[EntityId]) -> t.MutableMapping[str, t.Any]:
        return dict(
            current_entity=current_entity,
            current_path=request.path,
            petnames=self.petname_registry.get_petnames(viewer=current_entity) if (current_entity is not None) else {},
        )

    async def get_index(self, request: web.BaseRequest) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        markets = self.marketplace.get_public_markets()
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("index.jinja.html").render(
                public_markets=markets,
                **self._render_kwargs(request, current_entity),
            ),
            content_type="text/html",
        )

    async def get_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("create-market.jinja.html").render(
                **self._render_kwargs(request, current_entity),
            ),
            content_type="text/html",
        )

    async def post_create_market(self, request: web.BaseRequest) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        post_data = await request.post()
        try:
            market_id = self.marketplace.register_market(CfarMarket(
                name=str(post_data["name"]),
                proposition=str(post_data["proposition"]),
                floor=Probability(ln_odds=float(str(post_data["floor"]))),
                ceiling=Probability(ln_odds=float(str(post_data["ceiling"]))),
                state=Probability(ln_odds=float(str(post_data["state"]))),
            ))
        except (ValueError, KeyError, TypeError) as e:
            return web.HTTPBadRequest(reason=str(e))
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("redirect.jinja.html").render(
                text="Market created!",
                dest=self.resources.market_path(id=market_id),
            ),
            content_type="text/html",
        )

    async def get_market(self, request: web.Request) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        market_id = MarketId(str(request.match_info["id"]))
        try:
            market = self.marketplace.get_market(market_id=market_id)
        except KeyError:
            return web.HTTPNotFound()
        return web.Response(
            status=200,
            body=self.jinja_env.get_template('view-market.jinja.html').render(
                market_id=market_id,
                market=market,
                stakes=dict(sorted(market.stakes.items(), key=lambda kv: max(kv[1].ln_winnings_if_yes, kv[1].ln_winnings_if_no), reverse=True)),
                **self._render_kwargs(request, current_entity),
            ),
            content_type="text/html",
        )

    async def post_market(self, request: web.Request) -> web.StreamResponse:
        current_entity = self._get_entity(Session(await aiohttp_session.get_session(request)))
        if current_entity is None:
            return web.HTTPUnauthorized(reason="You gotta be logged in!")
        post_data = await request.post()
        market_id = MarketId(str(request.match_info["id"]))
        try:
            self.marketplace.update_market(
                market_id=market_id,
                participant_id=current_entity,
                new_state=Probability(ln_odds=float(str(post_data["state"]))),
            )
        except KeyError:
            return web.HTTPNotFound()
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
            password = Password(str(post_data["password"]))
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))
        session.token = self.username_password_auth.login(
            username=username,
            password=password,
        )

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
        post_data = await request.post()
        redirect_to = str(post_data["redirectTo"])
        if session.token is not None:
            self.token_auth.expire_token(session.token)
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
            object_id = EntityId(str(post_data["object"]))
            petname = Petname(str(post_data["petname"]))
            redirect_to = str(post_data["redirectTo"])
        except KeyError as e:
            return web.HTTPBadRequest(reason=str(e))

        self.petname_registry.add_petname(current_entity, object_id, petname)

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
        viewed_entity_id = request.match_info["id"]
        return web.Response(
            status=200,
            body=self.jinja_env.get_template("view-entity.jinja.html").render(
                viewed_entity_id=viewed_entity_id,
                **self._render_kwargs(request, current_entity),
            ),
            content_type="text/html",
        )
