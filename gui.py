from main import symbolify_cards, parse_cards, BIG_JOKER_SYMBOL, LITTLE_JOKER_SYMBOL

card = '''
+------------------+
|                  |
| {}                |
|                  |
|                  |
|                  |
|                  |
|                  |
|                  |
|                  |
|                  |
|                  |
|                {} |
|                  |
+------------------+
'''

big_joker = '''
+------------------+
|                  |
| J                |
| O                |
| K                |
| E                |
| R                |
|                  |
|                J |
|                O |
|                K |
|                E |
|                R |
|                  |
+------------------+
'''

little_joker = '''
+------------------+
|                  |
| j                |
| o                |
| k                |
| e                |
| r                |
|                  |
|                j |
|                o |
|                k |
|                e |
|                r |
|                  |
+------------------+
'''

def make_card(c):
    if c is BIG_JOKER_SYMBOL:
        return big_joker
    elif c is LITTLE_JOKER_SYMBOL:
        return little_joker
    else:
        return card.format(c, c)

def make_cards(cards):
    cards = symbolify_cards(cards)
    return list(map(make_card, cards))

def merge_cards(cards):
    cards = list(map(lambda s: s.splitlines(), cards))

    s = [''] * 16
    for n in range(16):
        for i, c in enumerate(cards):
            sep = 4 * i
            s[n] = s[n][:sep] + c[n]

    return "\n".join(s)
            
if __name__ == '__main__':
    res = merge_cards(make_cards(parse_cards("lb22aa33jkq45690")))
    print(res)
