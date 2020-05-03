import collections
import secrets
import typing as t

import grpc
import plauth  # type: ignore

from ...marketplace import Marketplace

from .protobuf.service_pb2_grpc import EntityServicer
from .protobuf import service_pb2 as proto


Username = t.NewType("Username", str)
EntityId = t.NewType("EntityId", str)
Token = t.NewType("Token", str)

class EntityServer(EntityServicer):
    def __init__(self) -> None:
        self.bcrypt_entities: t.MutableMapping[EntityId, plauth.AnybodyWithThisBcryptInverse] = {}
        self.username_to_entity_id: t.MutableMapping[Username, EntityId] = collections.defaultdict(lambda: EntityId("-".join(random_words(4, rng=self.rng))))
        self.token_to_entity: t.MutableMapping[Token, EntityId] = {}

    def UsernamePasswordLogin(self, request: proto.UsernamePasswordLoginRequest, context: grpc.ServicerContext) -> proto.UsernamePasswordLoginResponse:
        print(request, context)
        entity_id = self.username_to_entity_id[username]
        if entity_id not in self.bcrypt_entities:
            self.bcrypt_entities[entity_id] = plauth.AnybodyWithThisBcryptInverse.from_password(password)
        if self.bcrypt_entities[entity_id].check_password(password).accepted:
            token = secrets.token_urlsafe(16)  # TODO: is 16 enough?
            self.token_to_entity[token] = entity_id
            return proto.CreateMarketResponse(token=token)
        return grpc.Status(grpc.StatusCode.INVALID_ARGUMENT, "")

    def GetEntityForToken(self, request: proto.GetEntityForTokenRequest, context: grpc.ServicerContext) -> proto.GetEntityForTokenResponse:
        entity_id = self.token_to_entity.get(request.token)
        if entity_id is not None:
            return proto.GetEntityForTokenResponse(entity_id=entity_id)
        return proto.Status(grpc.StatusCode.INVALID_ARGUMENT, "")

    def DeleteToken(self, request: proto.DeleteTokenRequest, context: grpc.ServicerContext) -> proto.DeleteTokenResponse:
        self.token_to_entity.pop(request.token, None)
