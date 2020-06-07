module LoginWidget exposing (main)

import Browser
import Html exposing (Html, Attribute, text, button, div, input, span, a)
import Html.Attributes exposing (placeholder, value, disabled, style, href, type_)
import Html.Events exposing (keyCode, on, onClick, onInput)
import Http
import Json.Decode as D
import Json.Encode as E

type alias Username = String
type alias Password = String
type alias EntityId = String

type alias Model =
    { entity : Maybe EntityId
    , pendingRequest : Bool
    , usernameField : Username
    , passwordField : Password
    , error : Maybe String
    }

type Msg
    = SendLoginRequest
    | SendLogoutRequest
    | LoginRequestCompleted (Result Http.Error {entity : EntityId})
    | LogoutRequestCompleted (Result Http.Error ())
    | SetUsername Username
    | SetPassword Password
    | Ignore

main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = always Sub.none
        }

init : () -> ( Model , Cmd Msg )
init () =
    ( { entity = Nothing
      , pendingRequest = False
      , usernameField = ""
      , passwordField = ""
      , error = Nothing
      }
    , Cmd.none
    )

update : Msg -> Model -> ( Model , Cmd Msg )
update msg model =
    case msg of
        Ignore -> ( model , Cmd.none )
        SetUsername username -> ( {model | usernameField=username}, Cmd.none )
        SetPassword password -> ( {model | passwordField=password}, Cmd.none )
        SendLoginRequest ->
            if model.pendingRequest
                then ( Debug.log "ignoring command to send login request" model , Cmd.none )
                else ( {model | pendingRequest=True, error=Nothing} , sendLoginRequest model.usernameField model.passwordField)
        SendLogoutRequest ->
            if model.pendingRequest
                then ( Debug.log "ignoring command to send logout request" model , Cmd.none )
                else ( {model | pendingRequest=True, error=Nothing} , sendLogoutRequest)
        LoginRequestCompleted result ->
            case result of
                Err e -> Debug.log (Debug.toString e)
                    ( {model | pendingRequest=False, error=Just (Debug.toString e)}
                    , Cmd.none
                    )
                Ok {entity} ->
                    ( { model
                      | entity = Just entity
                      , pendingRequest = False
                      , error = Nothing
                      , usernameField = ""
                      , passwordField = ""
                      }
                    , Cmd.none
                    )
        LogoutRequestCompleted result ->
            case result of
                Err e -> Debug.log (Debug.toString e)
                    ( {model | pendingRequest=False, error=Just (Debug.toString e)}
                    , Cmd.none
                    )
                Ok () ->
                    ( { model | entity=Nothing, pendingRequest=False, error=Nothing }
                    , Cmd.none
                    )

sendLoginRequest : Username -> Password -> Cmd Msg
sendLoginRequest username password =
    Http.post
        { url = "/api/v1/username_login"
        , body = Http.jsonBody <| E.object [("username", E.string username), ("password", E.string password)]
        , expect = Http.expectJson LoginRequestCompleted (D.map (\s -> {entity=s}) <| D.field "entityId" D.string)
        }

sendLogoutRequest : Cmd Msg
sendLogoutRequest =
    Http.post
        { url = "/api/v1/logout"
        , body = Http.jsonBody <| E.object []
        , expect = Http.expectJson LogoutRequestCompleted (D.succeed ())
        }

view : Model -> Html Msg
view model =
    case model.entity of
        Nothing ->
            div []
                [ input
                    [ placeholder "username"
                    , onInput SetUsername
                    , value model.usernameField
                    , onEnter SendLoginRequest
                    , disabled model.pendingRequest
                    , style "max-width" "10em"
                    ]
                    []
                , input
                    [ type_ "password"
                    , placeholder "password"
                    , onInput SetPassword
                    , value model.passwordField
                    , onEnter SendLoginRequest
                    , disabled model.pendingRequest
                    , style "max-width" "10em"
                    ]
                    []
                , button
                    [ disabled model.pendingRequest
                    , onClick SendLoginRequest
                    ]
                    [ text "Log in" ]
                , case model.error of
                    Just errText -> div [] [span [style "color" "red"] [text errText]]
                    Nothing -> text ""
                ]
        Just entity ->
            div []
                [ text "Logged in as "
                , viewEntity entity
                , text " "
                , button [onClick SendLogoutRequest] [text "Log out"]
                ]

viewEntity : EntityId -> Html Msg
viewEntity entity =
    a [href ("/entity/" ++ entity)] [text entity]

onEnter : Msg -> Attribute Msg
onEnter msg =
    on "keydown" (D.map (\n -> if n == 13 then msg else Ignore) keyCode)
