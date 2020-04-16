import asyncio
import functools
import re

from aiohttp import web

import pytest  # type: ignore

from predictionmarkets.server import Server

@pytest.fixture
async def client(aiohttp_client):
    server = Server()
    app = web.Application()
    app.add_routes(server.routes())
    yield await aiohttp_client(app)


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
    body = await resp.text()
    id = re.search(r"/market/([a-z-]+)", body).group(1)

    resp = await client.get(f"/market/{id}")
    body = await resp.text()
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

    resp = await client.get("/")
    body = await resp.text()
    assert "MyName" in body
