module MarketList exposing (main)

import Browser
import Dict exposing (Dict)
import Html exposing (Html, text, input, strong, li, a, span, div, button, ul)
import Html.Attributes exposing (href, value, type_, style, min, max, step, disabled)
import Html.Events exposing (onClick)
import Http

import Endpoints
import Predictionmarkets.Marketplace as Marketplace
import OrderedDict exposing (OrderedDict)

type alias MarketId = String
type alias Market =
    { name : String
    , details : String
    }

type alias Model =
    { markets : OrderedDict MarketId Market
    , isLoading : Bool
    }

type Msg
    = LoadMoreRequested
    | LoadCompleted (Result Http.Error Marketplace.ListMarketsResponse)
    | Ignore

main = Browser.element
    { init = init
    , view = view
    , update = update
    , subscriptions = always Sub.none
    }

init : () -> ( Model , Cmd Msg )
init () =
    ( { markets = OrderedDict.empty
      , isLoading = True
      }
    , Endpoints.listMarkets LoadCompleted {limit=10, offset=0}
    )

view : Model -> Html Msg
view model =
    div []
        [ model.markets |> OrderedDict.toList |> List.map (\(id, m) -> li [] [viewMarket id m]) |> ul []
        , button [onClick LoadMoreRequested , disabled model.isLoading] [text "Load more"]
        ]

viewMarket : MarketId -> Market -> Html Msg
viewMarket id market =
    span []
        [ a [href ("/market/" ++ id)] [strong [] [text market.name]]
        , text " -- "
        , text market.details
        ]


onlyJusts : List (Maybe a) -> List a
onlyJusts mxs =
    let
        maybePrepend : Maybe a -> List a -> List a
        maybePrepend mx xs =
            case mx of
                Just x -> x :: xs
                Nothing -> xs
    in
        List.foldl maybePrepend [] mxs
        |> List.reverse

update : Msg -> Model -> ( Model , Cmd Msg )
update msg model =
    case msg of

        LoadMoreRequested ->
            ( {model | isLoading = True}
            , Endpoints.listMarkets LoadCompleted {limit=10, offset=(OrderedDict.size model.markets)}
            )

        LoadCompleted (Ok response) ->
            ( { model
              | isLoading = False
              , markets = OrderedDict.union model.markets
                    ( response.marketInfos
                    |> Dict.toList
                    |> List.map (\(k,mv) -> Maybe.map (\v -> (k,v)) mv)
                    |> onlyJusts
                    |> OrderedDict.fromList
                    )
              }
            , Cmd.none
            )

        LoadCompleted (Err e) -> Debug.todo (Debug.toString e)

        Ignore -> ( model , Cmd.none )
