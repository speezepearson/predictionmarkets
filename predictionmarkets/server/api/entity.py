import collections
import random
import secrets
import typing as t

import grpc  # type: ignore
import plauth  # type: ignore

from ...marketplace import Marketplace
from ...words import random_words

from .protobuf.service_pb2_grpc import EntityServicer
from .protobuf import service_pb2 as proto


Username = t.NewType("Username", str)
EntityId = t.NewType("EntityId", str)
Token = t.NewType("Token", str)

class EntityServer(EntityServicer):
    def __init__(self, rng: t.Optional[random.Random] = None) -> None:
        self.rng = rng if (rng is not None) else random.Random()
        self.bcrypt_entities: t.MutableMapping[EntityId, plauth.AnybodyWithThisBcryptInverse] = {}
        self.username_to_entity_id: t.MutableMapping[Username, EntityId] = collections.defaultdict(lambda: EntityId("-".join(random_words(4, rng=self.rng))))
        self.token_to_entity: t.MutableMapping[Token, EntityId] = {}

    def UsernamePasswordLogin(self, request: proto.UsernamePasswordLoginRequest, context: grpc.ServicerContext) -> proto.UsernamePasswordLoginResponseOrError:
        print('UsernamePasswordLogin request', request, 'context', context)
        entity_id = self.username_to_entity_id[Username(request.username)]
        if entity_id not in self.bcrypt_entities:
            self.bcrypt_entities[entity_id] = plauth.AnybodyWithThisBcryptInverse.from_password(request.password)
        if self.bcrypt_entities[entity_id].check_password(request.password).accepted:
            token = Token(secrets.token_urlsafe(16))  # TODO: is 16 enough?
            self.token_to_entity[token] = entity_id
            return proto.UsernamePasswordLoginResponseOrError(success=proto.UsernamePasswordLoginResponse(token=token))
        return proto.UsernamePasswordLoginResponseOrError(error=proto.RpcError(http_status=403))

    def GetEntityForToken(self, request: proto.GetEntityForTokenRequest, context: grpc.ServicerContext) -> proto.GetEntityForTokenResponseOrError:
        print('GetEntityForToken request', request, 'context', context)
        entity_id = self.token_to_entity.get(Token(request.token))
        if entity_id is not None:
            return proto.GetEntityForTokenResponseOrError(success=proto.GetEntityForTokenResponse(entity_id=entity_id))
        return proto.GetEntityForTokenResponseOrError(error=proto.RpcError(http_status=404))

    def DeleteToken(self, request: proto.DeleteTokenRequest, context: grpc.ServicerContext) -> proto.DeleteTokenResponseOrError:
        if request.token is not None:
            self.token_to_entity.pop(Token(request.token), None)
        return proto.DeleteTokenResponseOrError(success=proto.DeleteTokenResponse())
