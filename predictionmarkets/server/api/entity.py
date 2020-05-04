import collections
import random
import secrets
import typing as t

import plauth  # type: ignore

from ...marketplace import Marketplace
from ...words import random_words


Username = t.NewType("Username", str)
EntityId = t.NewType("EntityId", str)
Token = t.NewType("Token", str)

class EntityService:
    def __init__(self, rng: t.Optional[random.Random] = None) -> None:
        self.rng = rng if (rng is not None) else random.Random()
        self.bcrypt_entities: t.MutableMapping[EntityId, plauth.AnybodyWithThisBcryptInverse] = {}
        self.username_to_entity_id: t.MutableMapping[Username, EntityId] = collections.defaultdict(lambda: EntityId("-".join(random_words(4, rng=self.rng))))
        self.token_to_entity: t.MutableMapping[Token, EntityId] = {}

    def username_password_login(self, username: Username, password: str) -> Token:
        entity_id = self.username_to_entity_id[Username(username)]

        if entity_id not in self.bcrypt_entities:
            self.bcrypt_entities[entity_id] = plauth.AnybodyWithThisBcryptInverse.from_password(password)

        if self.bcrypt_entities[entity_id].check_password(password).accepted:
            token = Token(secrets.token_urlsafe(16))  # TODO: is 16 enough?
            self.token_to_entity[token] = entity_id
            return token
        raise ValueError("bad password")

    def get_entity_for_token(self, token: Token) -> t.Optional[EntityId]:
        entity_id = self.token_to_entity.get(Token(token))
        if entity_id is not None:
            return entity_id
        raise KeyError(token)

    def expire_token(self, token: Token) -> None:
        self.token_to_entity.pop(token, None)
