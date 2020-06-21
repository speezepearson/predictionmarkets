module Endpoints exposing
    ( listMarkets
    , usernameLogIn
    , logOut
    )

import Http

import Protobuf.Encode
import Protobuf.Decode

import Predictionmarkets.Auth as Auth
import Predictionmarkets.Marketplace as Marketplace

type alias Endpoint req resp =
    { encoder : req -> Protobuf.Encode.Encoder
    , decoder : Protobuf.Decode.Decoder resp
    , url : String
    }

hit : Endpoint req resp -> (Result Http.Error resp -> msg) -> req -> Cmd msg
hit endpoint toMsg req =
    Http.post
        { url = endpoint.url
        , body = Http.bytesBody "application/octet-stream"
            <| Protobuf.Encode.encode
            <| endpoint.encoder req
        , expect = Protobuf.Decode.expectBytes toMsg (endpoint.decoder)
        }

listMarkets : (Result Http.Error Marketplace.ListMarketsResponse -> msg) -> Marketplace.ListMarketsRequest -> Cmd msg
listMarkets =
    hit
        { encoder = Marketplace.toListMarketsRequestEncoder
        , decoder = Marketplace.listMarketsResponseDecoder
        , url = "/api/v1/list_markets"
        }

usernameLogIn : (Result Http.Error Auth.UsernameLogInResponse -> msg) -> Auth.UsernameLogInRequest -> Cmd msg
usernameLogIn =
    hit
        { encoder = Auth.toUsernameLogInRequestEncoder
        , decoder = Auth.usernameLogInResponseDecoder
        , url = "/api/v1/username_log_in"
        }

logOut : (Result Http.Error Auth.LogOutResponse -> msg) -> Auth.LogOutRequest -> Cmd msg
logOut =
    hit
        { encoder = Auth.toLogOutRequestEncoder
        , decoder = Auth.logOutResponseDecoder
        , url = "/api/v1/log_out"
        }
