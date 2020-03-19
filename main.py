"""
针对残局模式，有两个玩家参与，me 和 op。因为是零和博弈，所以在给定牌面的情况下，其中一方必胜。

每个人手中都有牌（cards），每次都可能打出（play）一手牌（hand），也可以选择不要（pass）
"""

from itertools import combinations
from itertools import chain
from functools import lru_cache
import gui

from enum import Enum, unique

@unique
class HandKind(Enum):
    ALL = -1
    PASS = 0
    PLANE_PLUS_DOUBLE = 1        # >= 10
    PLANE_PLUS_SINGLE = 2        # >= 8
    QUADRUPLE_PLUS_DOUBLE = 3    # 8
    PLANE = 4                    # >= 6
    DOUBLE_STRAIGHT = 5          # >= 6
    QUADRUPLE_PLUS_SINGLE = 6    # 6
    STRAIGHT = 7                 # >= 5
    TRIPLE_PLUS_DOUBLE = 8       # 5
    TRIPLE_PLUS_SINGLE = 9       # 4
    BOMB = 10                    # 4
    TRIPLE = 11                  # 3
    DOUBLE = 12                  # 2
    ROCKET = 13                  # 2
    SINGLE = 14                  # 1


symbol_level_map = {
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 10,
    "J": 11,  # Jack
    "Q": 12,  # Queen
    "K": 13,  # King
    "A": 14,  # Ace
    "2": 16,
    "L": 20,  # Little joker
    "B": 21,  # Big joker
}

level_symbol_map = {v: k for k, v in symbol_level_map.items()}

BIG_JOKER = symbol_level_map["B"]
LITTLE_JOKER = symbol_level_map["L"]

BIG_JOKER_SYMBOL = level_symbol_map[BIG_JOKER]
LITTLE_JOKER_SYMBOL = level_symbol_map[LITTLE_JOKER]


def parse_cards(card_symbols):
    return tuple(map(lambda c: symbol_level_map[c], tuple(card_symbols.upper())))

def symbolify_cards(cards):
    return tuple(map(lambda c: level_symbol_map[c], tuple(cards)))

def cards_in(left, right):
    # if all cards in left is contained by right
    right_cards = list(right)
    for c in left:
        if c not in right_cards:
            return False
        right_cards.remove(c)

    return True

def cards_sub(left, right):
    # left - right
    assert cards_in(right, left), "there exist some cards in right which are not contained in left"

    left_cards = list(left)
    for c in right:
        left_cards.remove(c)

    return tuple(left_cards)


def get_hands(kind, cards):
    unique_cards = frozenset(cards)

    if kind is HandKind.PASS:
        yield (kind, ()), cards

    elif kind is HandKind.ALL:
        for k in HandKind:
            if k in (HandKind.PASS, HandKind.ALL):
                continue
            yield from get_hands(k, cards)

    elif kind is HandKind.SINGLE:
        for c in unique_cards:
            hand_cards = (c,)
            yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.STRAIGHT:
        min_len = 5
        max_len = len(unique_cards)

        for l in range(min_len, max_len + 1):
            for c in unique_cards:
                hand_cards = tuple(range(c, c + l))
                if cards_in(hand_cards, cards):
                    yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.DOUBLE:
        for c in unique_cards:
            hand_cards = (c,) * 2
            if cards_in(hand_cards, cards):
                yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.DOUBLE_STRAIGHT:
        min_len = 3
        max_len = len(unique_cards)

        for l in range(min_len, max_len + 1):
            for c in unique_cards:
                hand_cards = tuple(e for e in range(c, c+l) for i in range(2))
                if cards_in(hand_cards, cards):
                    yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.TRIPLE:
        for c in unique_cards:
            hand_cards = (c,) * 3
            if cards_in(hand_cards, cards):
                yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.TRIPLE_PLUS_SINGLE:
        for t, r in get_hands(HandKind.TRIPLE, cards):
            for s, rest in get_hands(HandKind.SINGLE, r):
                if t[1][0] != s[1][0]:
                    hand_cards = t[1] + s[1]
                    yield (kind, hand_cards), rest

    elif kind is HandKind.TRIPLE_PLUS_DOUBLE:
        for t, r in get_hands(HandKind.TRIPLE, cards):
            for d, rest in get_hands(HandKind.DOUBLE, r):
                hand_cards = t[1] + d[1]
                yield (kind, hand_cards), rest

    elif kind is HandKind.PLANE:
        min_len = 2
        max_len = len(unique_cards)

        for l in range(min_len, max_len + 1):
            for c in unique_cards:
                hand_cards = tuple(e for e in range(c, c + l) for i in range(3))
                if cards_in(hand_cards, cards):
                    yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.PLANE_PLUS_SINGLE:
        for p, rest in get_hands(HandKind.PLANE, cards):
            l = len(p[1]) // 3
            rest_singles = tuple(s[1] for s, _ in get_hands(HandKind.SINGLE, rest))

            for singles in combinations(rest_singles, l):
                singles = tuple(chain.from_iterable(singles))
                hand_cards = p[1] + singles
                yield (kind, hand_cards), cards_sub(rest, singles)

    elif kind is HandKind.PLANE_PLUS_DOUBLE:
        for p, rest in get_hands(HandKind.PLANE, cards):
            l = len(p[1]) // 3
            rest_doubles = tuple(d[1] for d, _ in get_hands(HandKind.DOUBLE, rest))

            for doubles in combinations(rest_doubles, l):
                doubles = tuple(chain.from_iterable(doubles))
                hand_cards = p[1] + doubles
                yield (kind, hand_cards), cards_sub(rest, doubles)

    elif kind is HandKind.BOMB:
        for c in unique_cards:
            hand_cards = (c,) * 4
            if cards_in(hand_cards, cards):
                yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.ROCKET:
        if LITTLE_JOKER in cards and BIG_JOKER in cards:
            hand_cards = (LITTLE_JOKER, BIG_JOKER)
            yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.QUADRUPLE_PLUS_SINGLE:
        for b, rest in get_hands(HandKind.BOMB, cards):
            l = 2
            rest_singles = tuple(s[1] for s, _ in get_hands(HandKind.SINGLE, rest))

            for singles in combinations(rest_singles, l):
                singles = tuple(chain.from_iterable(singles))
                hand_cards = b[1] + singles
                yield (kind, hand_cards), cards_sub(rest, singles)

    elif kind is HandKind.QUADRUPLE_PLUS_DOUBLE:
        for b, rest in get_hands(HandKind.BOMB, cards):
            l = 2
            rest_doubles = tuple(s[1] for s, _ in get_hands(HandKind.DOUBLE, rest))

            for doubles in combinations(rest_doubles, l):
                doubles = tuple(chain.from_iterable(doubles))
                hand_cards = b[1] + doubles
                yield (kind, hand_cards), cards_sub(rest, doubles)


def cmp_hands(left, right):
    left_kind, left_cards = left
    right_kind, right_cards = right

    assert left_kind == right_kind, 'can not compare different kind of hand'

    kind = left_kind
    
    # all HandKind, no ROCKET, no PASS, no ALL
    if kind in (HandKind.SINGLE,
                HandKind.DOUBLE,
                HandKind.TRIPLE, HandKind.TRIPLE_PLUS_SINGLE, HandKind.TRIPLE_PLUS_DOUBLE,
                HandKind.BOMB):
        return left_cards[0] > right_cards[0]
    elif kind in (HandKind.STRAIGHT,
                  HandKind.DOUBLE_STRAIGHT,
                  HandKind.PLANE, HandKind.PLANE_PLUS_SINGLE, HandKind.PLANE_PLUS_DOUBLE,
                  HandKind.QUADRUPLE_PLUS_SINGLE, HandKind.QUADRUPLE_PLUS_DOUBLE):
        return len(left_cards) == len(right_cards) and left_cards[0] > right_cards[0]


def possible_hand(cards, played_hand):
    """
    斗地主规则有 14 种牌型，
    - 单张 single
    - 顺子（至少5张） straight

    - 对子 double
    - 连对（至少3对） double straight

    - 三张 triple
    - 三带一 triple plus single
    - 三带对 triple plus double
    - 飞机（至少2个三张） plane
    - 飞机带单张 plane plus single
    - 飞机带对子 plane plus double

    - 炸弹 bomb
    - 火箭 rocket
    - 四带二 quadruple plus single
    - 四带两对 quadruple plus double

    其中只有相同牌型才能相互压制（炸弹，火箭除外）
    火箭无条件压制一切；
    其次，炸弹无条件压制其它牌型；
    炸弹可压制炸弹，大小由单张大小决定；
    对于相同牌型，大小同单张大小决定；
    对于三带，飞机带，四带，只需要三张，四张比较大，带的牌不比较大小；

    对方出牌后，可以选择不要；如果对方不要，
    """
    played_hand_kind, played_hand_cards = played_hand

    if played_hand_kind is HandKind.PASS:
        yield from get_hands(HandKind.ALL, cards)
        return

    if played_hand_kind is HandKind.ROCKET:
        yield from get_hands(HandKind.PASS, cards)
        return

    for hand, rest in get_hands(played_hand_kind, cards):
        if cmp_hands(hand, played_hand):
            yield hand, rest

    yield from get_hands(HandKind.PASS, cards)

    if played_hand_kind is not HandKind.BOMB:
        for hand, rest in get_hands(HandKind.BOMB, cards):
            yield hand, rest
    
    yield from get_hands(HandKind.ROCKET, cards)


@lru_cache(maxsize=None)
def max_search(me, op, played_hand):
    for hand, rest in possible_hand(me, played_hand):
        if len(rest) == 0 or min_search(rest, op, hand)[0] > 0:
            return 1, hand
    else:
        return -1, None

@lru_cache(maxsize=None)
def min_search(me, op, played_hand):
    for hand, rest in possible_hand(op, played_hand):
        if len(rest) == 0 or max_search(me, rest, hand)[0] < 0:
            return -1, hand
    else:
        return 1, None


if __name__ == '__main__':
    #op, me = situations[0]
    
    op = input("Input op cards: ").strip()
    me = input("Input me cards: ").strip()
    
    op = tuple(sorted(parse_cards(op), reverse=True))
    me = tuple(sorted(parse_cards(me), reverse=True))

    print(op, me)

    played_hand = (HandKind.PASS, ())

    gui.display_table(me, op, played_hand, 'op')

    while True:
        score, played_hand = max_search(me, op, played_hand)

        if score > 0:
            me = cards_sub(me, played_hand[1])

            if len(me) == 0:
                print('success')
                break

            print("me play: {}".format(symbolify_cards(played_hand[1])))
            gui.display_table(me, op, played_hand, 'me')

            while True:
                p = input("op play: ").strip()
                p = parse_cards(p)

                legal = False

                for hand, rest in possible_hand(op, played_hand):
                    if sorted(hand[1]) == sorted(p):
                        played_hand = hand
                        op = rest
                        
                        print("op play: ", hand[1])
                        gui.display_table(me, op, played_hand, 'op')

                        import time
                        time.sleep(1)

                        legal = True
                        break

                if legal:
                    break
                
                print("op can't play like that")
        else:
            print("You can't win in this situation. :(")
            break

