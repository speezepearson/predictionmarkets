module OrderedDict exposing
    ( OrderedDict
    , empty
    , singleton
    , get
    , insert
    , isEmpty
    , first
    , last
    , member
    , union
    , toList
    , fromList
    , size
    )

import Dict exposing (Dict)

type OrderedDict k v = OrderedDict
    { dict : Dict k v
    , next : Dict k k
    , ends : Maybe (k, k)
    }

empty : OrderedDict comparable v
empty = OrderedDict {dict=Dict.empty, next=Dict.empty, ends=Nothing}

isEmpty : OrderedDict comparable v -> Bool
isEmpty (OrderedDict {ends}) =
    ends == Nothing

size : OrderedDict comparable v -> Int
size (OrderedDict {dict}) =
    Dict.size dict

singleton : comparable -> v -> OrderedDict comparable v
singleton k v =
    OrderedDict {dict=Dict.singleton k v, next=Dict.empty, ends=Just (k, k)}

iterate : (a -> Maybe a) -> Maybe a -> List a
iterate f mx =
    case mx of
        Nothing -> []
        Just x -> x :: iterate f (f x)

toList : OrderedDict comparable v -> List (comparable, v)
toList (OrderedDict od) =
    let
        must : Maybe a -> a
        must mx = case mx of
            Just x -> x
            Nothing -> Debug.todo "impossible"
    in
        od.ends
        |> Maybe.map Tuple.first
        |> iterate (\k -> Dict.get k od.next)
        |> List.map (\k -> (k, must (Dict.get k od.dict)))

fromList : List (comparable, v) -> OrderedDict comparable v
fromList kvs =
    List.foldl (\(k, v) acc -> insert k v acc) empty kvs

first : OrderedDict comparable v -> Maybe comparable
first (OrderedDict {ends}) =
    Maybe.map Tuple.first ends

last : OrderedDict comparable v -> Maybe comparable
last (OrderedDict {ends}) =
    Maybe.map Tuple.second ends

member : comparable -> OrderedDict comparable v -> Bool
member k (OrderedDict {dict}) =
    Dict.member k dict

get : comparable -> OrderedDict comparable v -> Maybe v
get k (OrderedDict {dict}) =
    Dict.get k dict

insert : comparable -> v -> OrderedDict comparable v -> OrderedDict comparable v
insert k v (OrderedDict od) =
    if Dict.member k od.dict then
        OrderedDict { od | dict = od.dict |> Dict.insert k v}
    else case od.ends of
        Nothing -> singleton k v
        Just (fst, lst) ->
            OrderedDict
                { od
                | dict = od.dict |> Dict.insert k v
                , next = od.next |> Dict.insert lst k
                , ends = Just (fst, k)
                }

union : OrderedDict comparable v -> OrderedDict comparable v -> OrderedDict comparable v
union d1 d2 =
    fromList <| List.concat [toList d1 , toList d2]
