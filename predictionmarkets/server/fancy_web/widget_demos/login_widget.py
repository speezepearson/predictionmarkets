from pathlib import Path

from aiohttp import web

from ... import api
from ...api.protobuf.predictionmarkets import auth_pb2

user_passwords = {
    "alice": "a",
    "bob": "b",
}

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
    app = web.Application()
    app.add_routes(routes)
    app.add_routes(api.make_routes(
        list_markets_func=None,
        username_log_in_func=(lambda username, password: username if password == user_passwords.get(username) else raise_(web.HTTPUnauthorized())),
        log_out_func=None,
    ))
    web.run_app(app, host='localhost', port=8080)
