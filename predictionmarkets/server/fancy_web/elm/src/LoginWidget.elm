port module LoginWidget exposing (main)

import Browser
import Html exposing (Html, Attribute, text, button, div, input, span, a)
import Html.Attributes exposing (placeholder, value, disabled, style, href, type_)
import Html.Events exposing (keyCode, on, onClick, onInput)
import Http

import Json.Decode

import Endpoints

type alias Username = String
type alias Password = String
type alias EntityId = String

type alias Flags =
    { entity : Maybe EntityId
    }

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
    | LoginRequestCompleted (Result Http.Error {entityId : EntityId})
    | LogoutRequestCompleted (Result Http.Error {})
    | SetUsername Username
    | SetPassword Password
    | Ignore

port loggedIn : EntityId -> Cmd msg
port loggedOut : () -> Cmd msg

main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = always Sub.none
        }

init : Flags -> ( Model , Cmd Msg )
init flags =
    ( { entity = flags.entity
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
            if model.pendingRequest then
                ( Debug.log "ignoring command to send login request" model
                , Cmd.none
                )
            else
                ( { model | pendingRequest=True, error=Nothing }
                , Endpoints.usernameLogIn LoginRequestCompleted {username=model.usernameField, password=model.passwordField}
                )
        SendLogoutRequest ->
            if model.pendingRequest then
                ( Debug.log "ignoring command to send logout request" model
                , Cmd.none
                )
            else
                ( { model | pendingRequest=True, error=Nothing }
                , Endpoints.logOut LogoutRequestCompleted {}
                )
        LoginRequestCompleted (Err e) ->
            ( {model | pendingRequest=False, error=Just (Debug.toString e)}
            , Cmd.none
            )
            |> Debug.log (Debug.toString e)

        LoginRequestCompleted (Ok {entityId}) ->
            ( { model
              | entity = Just entityId
              , pendingRequest = False
              , error = Nothing
              , usernameField = ""
              , passwordField = ""
              }
            , loggedIn entityId
            )
        LogoutRequestCompleted result ->
            case result of
                Err e -> Debug.log (Debug.toString e)
                    ( {model | pendingRequest=False, error=Just (Debug.toString e)}
                    , Cmd.none
                    )
                Ok {} ->
                    ( { model | entity=Nothing, pendingRequest=False, error=Nothing }
                    , loggedOut ()
                    )

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
    on "keydown" (Json.Decode.map (\n -> if n == 13 then msg else Ignore) keyCode)
