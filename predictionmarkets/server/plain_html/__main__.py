import argparse
import random

from aiohttp import web
import aiohttp_session  # type: ignore

from plauth.authenticator import TokenAuthenticator, UsernamePasswordAuthenticator, EntityId

from ... import Probability, CfarMarket, Marketplace, MarketId
from ...marketplace import Marketplace
from ...petnames import Petname, PetnameRegistry
from . import Server, Resources
from ...words import random_words


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=8080)
parser.add_argument("-H", "--host", default="localhost")
parser.add_argument("--random-seed", type=int, default=None)
args = parser.parse_args()

rng = random.Random()
if args.random_seed is not None:
    rng.seed(args.random_seed)

token_auth = TokenAuthenticator()

app = web.Application()
aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
html_server = Server(
    token_auth=token_auth,
    username_password_auth=UsernamePasswordAuthenticator(
        make_random_entity_id=(lambda: EntityId("-".join(random_words(4)))),
        token_authenticator=token_auth,
    ),
    marketplace=Marketplace(rng=rng),
    petname_registry=PetnameRegistry(),
    resources=Resources(app.router),
)
html_server.add_handlers()

web.run_app(app, host=args.host, port=args.port)
