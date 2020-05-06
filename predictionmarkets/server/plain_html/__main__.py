import argparse
import random

from aiohttp import web
import aiohttp_session  # type: ignore

from ... import Probability, CfarMarket, Marketplace, MarketId
from ..api.marketplace import MarketplaceService  # type: ignore
from ..api.entity import EntityService, Token, EntityId, Username  # type: ignore
from ..api.petname import Petname, PetnameService
from . import Server, Resources


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=8080)
parser.add_argument("-H", "--host", default="localhost")
parser.add_argument("--random-seed", type=int, default=None)
args = parser.parse_args()

rng = random.Random()
if args.random_seed is not None:
    rng.seed(args.random_seed)
marketplace = Marketplace(rng=rng)

entity_service = EntityService(rng=rng)
market_service = MarketplaceService(marketplace=marketplace)

app = web.Application()
aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
html_server = Server(
    entity_service=entity_service,
    market_service=market_service,
    petname_service=PetnameService(),
    resources=Resources(app.router),
)
html_server.add_handlers()

web.run_app(app, host=args.host, port=args.port)
