import asyncio
import functools
import re

from aiohttp import web
from aiohttp.client import ClientSession
import bs4  # type: ignore
import pytest  # type: ignore
import aiohttp_session  # type: ignore

from predictionmarkets import Marketplace
from predictionmarkets.server.plain_html import Server, MarketResources
from predictionmarkets.server.api.entity import EntityService
from predictionmarkets.server.api.marketplace import MarketplaceService

@pytest.fixture
async def client(aiohttp_client):
    app = web.Application()
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
    Server(
        entity_service=EntityService(),
        market_service=MarketplaceService(Marketplace()),
        resources=MarketResources(app.router),
    ).add_handlers()
    yield await aiohttp_client(app)

async def check_links(client: ClientSession, html: str) -> str:
    soup = bs4.BeautifulSoup(html, "html.parser")
    for tag in soup.select("[href]"):
        assert (await client.get(tag["href"])).status == 200

    return html

async def test_create(client):
    resp = await client.post(
        "/create-market",
        data={
            "name": "MyName",
            "proposition": "MyProposition",
            "floor": -10,
            "ceiling": 10,
            "state": 3,
        })
    assert resp.status == 200
    body = await check_links(client, await resp.text())
    [id] = {m.group(1) for m in re.finditer(r"/market/([a-z-]+)", body)}

    resp = await client.get(f"/market/{id}")
    body = await check_links(client, await resp.text())
    assert "MyName" in body
    assert "MyProposition" in body

async def test_created_market_appears_on_index(client):
    resp = await client.post(
        "/create-market",
        data={
            "name": "MyName",
            "proposition": "MyProposition",
            "floor": -10,
            "ceiling": 10,
            "state": 3,
        })
    assert resp.status == 200
    await check_links(client, await resp.text())

    resp = await client.get("/")
    body = await check_links(client, await resp.text())
    assert "MyName" in body
