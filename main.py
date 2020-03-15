from itertools import combinations
from itertools import chain

'''
概念定义：

针对残局模式，有两个玩家 player 参与，me 和 op。因为是零和博弈，所以在给定牌面的情况下，其中一方必胜。

每个人手中都有牌（cards），每次都可能打出（play）一手牌（hand），也可以选择不要（pass）
'''



if __name__ == '__main__':
    # poker symbol to underline number
    sym_num = {
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 10,
        "J": 11, # Jack
        "Q": 12, # Queen
        "K": 13, # King
        "A": 14, # Ace
        "2": 16,
        "L": 20, # Little joker
        "B": 21, # Big joker
    }

    num_sym = {v: k for k, v in sym_num.items()}

    def get_poker(s):
        return list(map(lambda c: sym_num[c], list(s)))

    def all_play(poker):
        '''
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

        对方出牌后，可以选择不要；如果对方不要，自己必须要出牌；
        '''
        for p in poker:
            c = poker.copy()
            c.remove(p)
            yield p, c

    def cards_in(left, right):
        # if all cards in left is contained by right
        pass

    def cards_sub(left, right):
        # left - right
        pass

    def get_hands(kind, cards):
        '''
        kind: all 14, pass, all(except pass)
        '''
        if kind == 'pass':
            yield ('pass',), cards.copy()
            
        elif kind == 'all':
            # todo: yield all kind except pass
            pass
        
        elif kind == 'single':
            for c in set(cards):
                s = [c]
                yield (kind, s), cards_sub(cards, s)

        elif kind == 'straight':
            unique_cards = list(set(cards))
            min_len = 5
            max_len = len(unique_cards)

            if max_len < min_len:
                return

            for l in range(min_len, max_len+1):
                for c in unique_cards:
                    s = list(range(c, c+l))
                    if cards_in(s, cards):
                        yield ('straight', s), cards_sub(cards, s)

        elif kind == 'double':
            unique_cards = list(set(cards))
            
            for c in unique_cards:
                d = [c] * 2
                if cards_in(d, cards):
                    yield ('double', d), cards_sub(cards, d)
            
        elif kind == 'double straight':
            unique_cards = list(set(cards))
            min_len = 3
            max_len = len(unique_cards)

            if max_len < min_len:
                return

            for l in range(min_len, max_len+1):
                for c in unique_cards:
                    s = list(range(c, c+l))
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

            for l in range(min_len, max_len+1):
                for c in unique_cards:
                    s = list(range(c, c+l))
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
            little = sym_num['L']
            big = sym_num['B']
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

        assert(kind == left_kind == right_kind, 'can not compare different kind of hand')

        # kind is 14 - rocket, no pass
        if kind == 'single':
            return left_cards[0] > right_cards[0]
        
                

    def possible_hand(cards, cur):
        # hand is (kind, *points)
        kind, *points = cur

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
        for play, rest in all_play(me):
            if not can_play(play, cur):
                continue
            
            if len(rest) == 0 or min_search(rest, op, play) > 0:
                return 1, play
        else:
            return -1, None

    def min_search(me, op, cur):
        for play, rest in all_play(op):
            if not can_play(play, cur):
                continue
            
            if len(rest) == 0 or max_search(me, rest, play)[0] < 0:
                return -1
        else:
            return 1


    me = input("my card: ").strip().upper()
    op = input("op card: ").strip().upper()

    me = get_poker(me)
    op = get_poker(op)

    def num_to_sym(n):
        return num_sym[n]

    exit()

    while True:
        score, play = max_search(me, op, None)

        if score > 0:
            me.remove(play)
            print("me play: {}".format(num_to_sym(play)))

            p = input("op play: ").strip()
            op.remove(sym_num[p])
        else:
            print("lose")
            break

