from .authenticator import *
from .entity import *
from .permissions import *

UrAuthenticator = BcryptAuthenticator(
    salt=b'$2b$12$zgkU9joHGw8AFfY25JH4tO',
    hashed=b'$2b$12$zgkU9joHGw8AFfY25JH4tOq0wsGxfbTX04VGr2UxXgwCdRAWkoL.e',
)
