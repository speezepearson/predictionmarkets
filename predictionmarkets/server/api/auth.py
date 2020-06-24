import argparse
import bcrypt
import contextvars
from pathlib import Path
from typing import Optional, NewType, Mapping
import secrets

from aiohttp import web
import aiohttp_session

from . import pb_decorator
from .protobuf.predictionmarkets import auth_pb2

Token = NewType('Token', str)

class Authenticator:
    def __init__(self):
        self.username_bcrypts = {
            'a': b'$2b$12$8LipqQrSxerD0AZOXd17Ke4KDFvF2i/u75fD3if4i5yiMByHTkflG',
        }
        self.token_to_entity: Mapping[Token, str] = {}
        self.session: contextvars.ContextVar[aiohttp_session.Session] = contextvars.ContextVar('session')

    def username_log_in(self, username: str, password: str) -> Optional[Token]:
        hashed = self.username_bcrypts.get(username)
        if (hashed is not None) and bcrypt.checkpw(password.encode('utf8'), hashed):
            token = Token(secrets.token_urlsafe(8)) # TODO: enough?
            self.token_to_entity[token] = username # TODO: indirect entity->username
            self.session.get()['auth_token'] = token
            return token
        else:
            raise web.HTTPForbidden()

    def log_out(self) -> None:
        response = web.Response(status=200)
        session = self.session.get()
        token = session.pop('auth_token', None)
        self.token_to_entity.pop(token, None)

    @web.middleware
    async def middleware(self, request: web.BaseRequest, handler: web.RequestHandler) -> web.StreamResponse:
        cv_token = self.session.set(await aiohttp_session.get_session(request))
        try:
            return await handler(request)
        finally:
            self.session.reset(cv_token)

def make_routes(
    authenticator: Authenticator,
) -> web.RouteTableDef:
    # TODO: fix this crummy signature

    routes = web.RouteTableDef()

    @routes.post('/api/v1/username_log_in')
    @pb_decorator.protobuf(auth_pb2.UsernameLogInRequest, auth_pb2.UsernameLogInResponse)
    async def username_log_in(
        request: web.BaseRequest,
        request_pb: auth_pb2.UsernameLogInRequest
    ) -> auth_pb2.UsernameLogInResponse:
        token = authenticator.username_log_in(username=request_pb.username, password=request_pb.password)
        return auth_pb2.UsernameLogInResponse(token=token)

    @routes.post('/api/v1/log_out')
    @pb_decorator.protobuf(auth_pb2.LogOutRequest, auth_pb2.LogOutResponse)
    async def log_out(
        request: web.BaseRequest,
        request_pb: auth_pb2.LogOutRequest
    ) -> auth_pb2.LogOutResponse:
        authenticator.log_out()
        return auth_pb2.LogOutResponse()

    return routes
