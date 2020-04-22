from __future__ import annotations
import bcrypt
import hashlib
import dataclasses
import typing as t

@dataclasses.dataclass(frozen=True)
class AuthVerdict:
    accepted: bool = False

C = t.TypeVar('C')
R = t.TypeVar('R')

class Authenticator(t.Generic[C, R]):
    def issue_challenge(self) -> C:
        pass
    def judge_response(self, response: R) -> AuthVerdict:
        pass

@dataclasses.dataclass(frozen=True)
class BcryptAuthenticator(Authenticator[None, str]):
    salt: bytes
    hashed: bytes

    def issue_challenge(self) -> None:
        pass

    def judge_response(self, password: str) -> AuthVerdict:
        return AuthVerdict(accepted=bcrypt.checkpw(password.encode("utf8"), self.hashed))

@dataclasses.dataclass(frozen=True)
class CookieAuthenticator(Authenticator[None, str]):
    salt: bytes
    cookie_hash: str

    def issue_challenge(self) -> None:
        pass

    def judge_response(self, cookie: str) -> AuthVerdict:
        actual = hashlib.sha256(cookie.encode("utf8") + self.salt).hexdigest()
        return AuthVerdict(accepted=(actual == self.cookie_hash))

__all__ = [
    AuthVerdict.__name__,
    Authenticator.__name__,
    BcryptAuthenticator.__name__,
    CookieAuthenticator.__name__,
]
