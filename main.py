import time

from algo import max_search, min_search
from rule import HandKind
from rule import filter_illegal_cards, parse_cards, symbolify_cards
from rule import possible_hand, cards_sub
from interface import display_table, display_cards


help_message = '''
输入扑克牌的规则如下：

     输入    含义
    1/a/A      A
      2       2
      3       3
      4       4
      5       5
      6       6
      7       7
      8       8
      8       9
      0      10
     j/J      J
     q/Q      Q
     k/K      K
     l/L     小王
     b/B     大王
    enter 输入结束/pass
'''

def gather_init_cards(msg):
    while True:
        card_symbols = input(msg).strip()
        illegal = filter_illegal_cards(card_symbols)

        if illegal:
            print("出现了规则外的输入 " + " ".join(illegal))
        else:
            break
            
    return tuple(sorted(parse_cards(card_symbols), reverse=True))
        
    
if __name__ == '__main__':
    print(help_message)

    op = gather_init_cards("对手的初始手牌 -> ")
    
    display_cards(op, 0, 'op')
    
    me = gather_init_cards("自己的初始手牌 -> ")
    
    display_cards(me, 0, 'me')
    
    time.sleep(1)

    played_hand = (HandKind.PASS, ())

    display_table(me, op, played_hand, 'op')

    while True:
        score, played_hand = max_search(me, op, played_hand)

        if score > 0:
            me = cards_sub(me, played_hand[1])

            display_table(me, op, played_hand, 'me')

            if len(me) == 0:
                break

            while True:
                op_played = input("\n对手打出的牌 -> ").strip()

                illegal = filter_illegal_cards(op_played)
                if illegal:
                    print("出现了规则外的输入 " + " ".join(illegal))
                    continue
                
                op_played = parse_cards(op_played)

                legal = False
                for hand, rest in possible_hand(op, played_hand):
                    if sorted(hand[1]) == sorted(op_played):
                        played_hand = hand
                        op = rest
                        
                        display_table(me, op, played_hand, 'op')

                        time.sleep(1)
                        legal = True
                        break
                if legal:
                    break
                
                print("无法这样出牌")
        else:
            print("\n这是一个必输的局面 :(")
            break

