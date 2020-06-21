import aiohttp_session
from pathlib import Path

from aiohttp import web

from ...api import auth
from ...api.protobuf.predictionmarkets import auth_pb2

routes = web.RouteTableDef()

@routes.get('/')
async def index(req):
    return web.FileResponse(Path(__file__).parent/'login_widget.html')

@routes.get('/static/LoginWidget.js')
async def index(req):
    return web.FileResponse(Path(__file__).parent.parent/'elm'/'dist'/'LoginWidget.js')

def raise_(e):
    raise e

if __name__ == '__main__':
    authenticator = auth.Authenticator()
    app = web.Application(middlewares=[
        aiohttp_session.session_middleware(aiohttp_session.SimpleCookieStorage()),
        authenticator.middleware,
    ])
    app.add_routes(routes)
    app.add_routes(auth.make_routes(authenticator))
    web.run_app(app, host='localhost', port=8080)
