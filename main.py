"""
针对残局模式，有两个玩家参与，me 和 op。因为是零和博弈，所以在给定牌面的情况下，其中一方必胜。

每个人手中都有牌（cards），每次都可能打出（play）一手牌（hand），也可以选择不要（pass）
"""

from itertools import combinations
from itertools import chain


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


def parse_cards(card_symbols):
    return list(map(lambda c: symbol_level_map[c], list(card_symbols)))


def cards_in(left, right):
    # if all cards in left is contained by right
    right_cards = right.copy()
    for c in left:
        if c not in right_cards:
            return False
        right_cards.remove(c)

    return True


def cards_sub(left, right):
    # left - right
    assert cards_in(right, left), "there exist some cards in right which are not contained in left"

    left_cards = left.copy()
    for c in right:
        left_cards.remove(c)

    return left_cards


from enum import Enum, unique

@unique
class HandKind(Enum):
    ALL = -1
    PASS = 0
    SINGLE = 1
    STRAIGHT = 2
    DOUBLE = 3
    DOUBLE_STRAIGHT = 4
    TRIPLE = 5
    TRIPLE_PLUS_SINGLE = 6
    TRIPLE_PLUS_DOUBLE = 7
    PLANE = 8
    PLANE_PLUS_SINGLE = 9
    PLANE_PLUS_DOUBLE = 10
    BOMB = 11
    ROCKET = 12
    QUADRUPLE_PLUS_SINGLE = 13
    QUADRUPLE_PLUS_DOUBLE = 14

def get_hands(kind, cards):
    unique_cards = list(set(cards))

    if kind is HandKind.PASS:
        yield (kind, []), cards.copy()

    elif kind is HandKind.ALL:
        # todo: yield all kind except pass
        pass

    elif kind is HandKind.SINGLE:
        for c in unique_cards:
            hand_cards = [c]
            yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.STRAIGHT:
        min_len = 5
        max_len = len(unique_cards)

        for l in range(min_len, max_len + 1):
            for c in unique_cards:
                hand_cards = list(range(c, c + l))
                if cards_in(hand_cards, cards):
                    yield (kind, hand_cards), cards_sub(cards, hand_cards)

    elif kind is HandKind.DOUBLE:
        for c in unique_cards:
            hand_cards = [c] * 2
            if cards_in(hand_cards, cards):
                yield (kind, hand_cards), cards_sub(cards, hand_cards)


    elif kind == 'double straight':
        unique_cards = list(set(cards))
        min_len = 3
        max_len = len(unique_cards)

        if max_len < min_len:
            return

        for l in range(min_len, max_len + 1):
            for c in unique_cards:
                s = list(range(c, c + l))
                ds = [e for e in s for i in range(2)]
                if cards_in(ds, cards):
                    yield ('double straight', ds), cards_sub(cards, ds)

    elif kind == 'triple':
        unique_cards = list(set(cards))

        for c in unique_cards:
            t = [c] * 3
            if cards_in(t, cards):
                yield ('double', t), cards_sub(cards, t)

    elif kind == 'triple plus single':
        for t, r in get_hands('triple', cards):
            for s, rest in get_hands('single', r):
                if t[1][0] != s[1][0]:
                    tps = t[1] + s[1]
                    yield ('triple plus single', tps), rest

    elif kind == 'triple plus double':
        for t, r in get_hands('triple', cards):
            for d, rest in get_hands('double', r):
                if t[1][0] != d[1][0]:
                    tpd = t[1] + d[1]
                    yield ('triple plus double', tpd), rest

    elif kind == 'plane':
        unique_cards = list(set(cards))
        min_len = 2
        max_len = len(unique_cards)

        for l in range(min_len, max_len + 1):
            for c in unique_cards:
                s = list(range(c, c + l))
                p = [e for e in s for i in range(3)]
                if cards_in(p, cards):
                    yield ('plane', p), cards_sub(cards, p)

    elif kind == 'plane plus single':
        for p, rest in get_hands('plane', cards):
            p_len = len(p[1]) // 3

            singles = [s[1] for s, _ in get_hands('single', rest)]

            for s in combinations(singles, p_len):
                s = chain.from_iterable(s)
                pps = p[1] + s
                yield ('plane plus single', pps), cards_sub(rest, s)

    elif kind == 'plane plus double':
        for p, rest in get_hands('plane', cards):
            p_len = len(p[1]) // 3

            doubles = [d[1] for d, _ in get_hands('double', rest)]

            for d in combinations(doubles, p_len):
                d = chain.from_iterable(d)
                ppd = p[1] + d
                yield ('plane plus double', ppd), cards_sub(rest, d)

    elif kind == 'bomb':
        unique_cards = list(set(cards))

        for c in unique_cards:
            b = [c] * 4
            if cards_in(d, cards):
                yield ('bomb', b), cards_sub(cards, b)

    elif kind == 'rocket':
        little = symbol_level_map['L']
        big = symbol_level_map['B']
        if little in cards and big in cards:
            r = [little, big]
            yield ('rocket', r), cards_sub(cards, r)

    elif kind == 'quadruple plus single':
        for q, rest in get_hands('bomb', cards):

            singles = [s[1] for s, _ in get_hands('single', rest)]

            for s in combinations(singles, 2):
                s = chain.from_iterable(s)
                qps = q[1] + s
                yield ('plane plus single', pps), cards_sub(rest, s)

    elif kind == 'quadruple plus double':
        for q, rest in get_hands('bomb', cards):

            doubles = [d[1] for d, _ in get_hands('double', rest)]

            for d in combinations(doubles, 2):
                d = chain.from_iterable(d)
                qpd = q[1] + d
                yield ('plane plus double', qpd), cards_sub(rest, d)


def cmp_hand(kind, left, right):
    left_kind, *left_cards = left
    right_kind, *right_cards = right

    assert kind == left_kind == right_kind, 'can not compare different kind of hand'

    # kind is 14 - rocket, no pass
    if kind == 'single':
        return left_cards[0] > right_cards[0]


def possible_hand(cards, cur):
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
    # hand is (kind, cards)
    kind, points = cur

    if kind == 'pass':
        yield from get_hands('all', cards)
        return
    else:
        yield from get_hands('pass', cards)

    if kind == 'rocket':
        return
    else:
        yield from get_hands(kind, cards)

    for hand, rest in get_hands(kind, cards):
        if cmp_hand(kind, hand, cur):
            yield hand, rest

    if kind != 'bomb':
        for hand, rest in get_hands('bomb', cards):
            yield hand, rest


def max_search(me, op, cur):
    for play, rest in possible_hand(me, cur):
        if len(rest) == 0 or min_search(rest, op, play) > 0:
            return 1, play
    else:
        return -1, None


def min_search(me, op, cur):
    for play, rest in possible_hand(op, cur):
        if len(rest) == 0 or max_search(me, rest, play)[0] < 0:
            return -1
    else:
        return 1


'''
me = input("Input my cards: ").strip().upper()
op = input("Input op cards: ").strip().upper()

me = parse_cards(me)
op = parse_cards(op)


    while True:
        score, play = max_search(me, op, None)

        if score > 0:
            me.remove(play)
            print("me play: {}".format(num_to_sym(play)))

            p = input("op play: ").strip()
            op.remove(symbol_level_map[p])
        else:
            print("lose")
            break
'''
