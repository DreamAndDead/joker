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

    def possible_hand(player, cur):
        # hand is (kind, c1, c2, c3, c4, *)
        kind, *cards = cur

        if kind == 'single':
            s = cards[0]

            
            

    def can_play(play, cur):
        if cur is None:
            return play is not None
        else:
            if play is None:
                return True
            else:
                return play > cur

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

