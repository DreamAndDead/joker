import os
import main

card = '''
┏━━━━━━━━━━━━━━━━━━┓
┃                  ┃
┃ {}                ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                  ┃
┃                {} ┃
┃                  ┃
┗━━━━━━━━━━━━━━━━━━┛
'''

big_joker = '''
┏━━━━━━━━━━━━━━━━━━┓
┃                  ┃
┃ J                ┃
┃ O                ┃
┃ K                ┃
┃ E                ┃
┃ R                ┃
┃                  ┃
┃                J ┃
┃                O ┃
┃                K ┃
┃                E ┃
┃                R ┃
┃                  ┃
┗━━━━━━━━━━━━━━━━━━┛
'''

little_joker = '''
┏━━━━━━━━━━━━━━━━━━┓
┃                  ┃
┃ j                ┃
┃ o                ┃
┃ k                ┃
┃ e                ┃
┃ r                ┃
┃                  ┃
┃                j ┃
┃                o ┃
┃                k ┃
┃                e ┃
┃                r ┃
┃                  ┃
┗━━━━━━━━━━━━━━━━━━┛
'''

'''



'''


widget_height = card.count('\n')

def single_card_widget(c):
    if c is main.BIG_JOKER_SYMBOL:
        return big_joker
    elif c is main.LITTLE_JOKER_SYMBOL:
        return little_joker
    else:
        return card.format(c, c)

def multi_card_widgets(cards):
    cards = main.symbolify_cards(cards)
    return list(map(single_card_widget, cards))

def merge_card_widgets(cards):
    cards = list(map(lambda s: s.splitlines(), cards))

    s = [''] * widget_height
    for n in range(widget_height):
        for i, c in enumerate(cards):
            sep = 4 * i
            s[n] = s[n][:sep] + c[n]

    return "\n".join(s)

def shift_card_widgets(card_widgets, length):
    lines = card_widgets.splitlines()
    shift_lines = map(lambda l: ' ' * length + l, lines)
    return "\n".join(shift_lines)

def display_cards(cards, shift=0):
    c = shift_card_widgets(merge_card_widgets(multi_card_widgets(cards)), shift)
    print(c)

def display_table(me, op, played_hand, by):
    os.system('clear')

    display_cards(op, 30)
    display_cards(played_hand[1], 15)
    display_cards(me)
            
if __name__ == '__main__':
    
    cards = main.parse_cards("bl22aa33jkq45690")
    print(display_cards(cards, 30))
