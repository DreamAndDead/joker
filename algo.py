from functools import lru_cache
from rule import possible_hand

@lru_cache(maxsize=None)
def max_search(me, op, played_hand):
    for hand, rest in possible_hand(me, played_hand):
        if len(rest) == 0 or min_search(rest, op, hand) > 0:
            return 1, hand
    else:
        return -1, None

@lru_cache(maxsize=None)
def min_search(me, op, played_hand):
    for hand, rest in possible_hand(op, played_hand):
        if len(rest) == 0 or max_search(me, rest, hand)[0] < 0:
            return -1
    else:
        return 1


