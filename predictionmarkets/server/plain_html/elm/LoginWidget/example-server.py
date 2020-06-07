"""Demo usage: python --open-browser $THIS_FILE
"""
import argparse
from pathlib import Path
import typing as t
from aiohttp import web

class Server:
    def __init__(self) -> None:
        pass

    def routes(self) -> t.Iterable[web.RouteDef]:
        return [
            web.get('/', self.index),
            web.get('/static/elm-js/{filename}', self.static_elm),
            web.post('/api/v1/username_login', self.user_login),
            web.post('/api/v1/logout', self.logout),
            # placeholder: add more route-defs here
        ]

    async def index(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.FileResponse(Path(__file__).parent/'src'/'index.html')

    async def static_elm(self, request: web.BaseRequest) -> web.StreamResponse:
        return web.FileResponse(Path(__file__).parent/'dist'/request.match_info['filename'])

    async def user_login(self, request: web.BaseRequest) -> web.StreamResponse:
        j = await request.json()
        if j['username'] == j['password']:
            return web.json_response({"entityId": j['username']})
        return web.HTTPUnauthorized()

    async def logout(self, request: web.BaseRequest) -> web.StreamResponse:
        j = await request.json()
        return web.json_response({})

parser = argparse.ArgumentParser()
parser.add_argument('--open-browser', action='store_true')
parser.add_argument('-p', '--port', type=int, default=8080)
parser.add_argument('-H', '--host', default='localhost')

if __name__ == '__main__':
    args = parser.parse_args()

    app = web.Application()
    app.add_routes(Server().routes())

    if args.open_browser:
        async def _open_browser(_):
            import webbrowser
            webbrowser.open(f'http://{args.host}:{args.port}')
        # in practice I still sometimes see Connection Refused :/
        app.on_startup.append(_open_browser)

    web.run_app(app, host=args.host, port=args.port)
