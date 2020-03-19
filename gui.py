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



me_pass_label = '''




.______      ___           _______.     _______.
|   _  \    /   \         /       |    /       |
|  |_)  |  /  ^  \       |   (----`   |   (----`
|   ___/  /  /_\  \       \   \        \   \    
|  |     /  _____  \  .----)   |   .----)   |   
| _|    /__/     \__\ |_______/    |_______/    
                                                




'''



op_pass_label = '''




     _______.     _______.     ___      .______   
    /       |    /       |    /   \     |   _  \  
   |   (----`   |   (----`   /  ^  \    |  |_)  | 
    \   \        \   \      /  /_\  \   |   ___/  
.----)   |   .----)   |    /  _____  \  |  |      
|_______/    |_______/    /__/     \__\ | _|      





'''


pass_label = {
    "me": me_pass_label,
    "op": op_pass_label,
}

widget_height = card.count('\n')

def stylish_card(card, style='op'):
    if style == 'me':
        card = card.replace('┏', '┌')
        card = card.replace('┓', '┐')
        card = card.replace('━', '─')
        card = card.replace('┃', '│')
        card = card.replace('┗', '└')
        card = card.replace('┛', '┘')
    elif style == 'op':
        card = card.replace('┌', '┏')
        card = card.replace('┐', '┓')
        card = card.replace('─', '━')
        card = card.replace('│', '┃')
        card = card.replace('└', '┗')
        card = card.replace('┘', '┛')

    return card

def single_card_widget(c, style):
    res = card.format(c, c)
    
    if c is main.BIG_JOKER_SYMBOL:
        res = big_joker
    elif c is main.LITTLE_JOKER_SYMBOL:
        res = little_joker

    return stylish_card(res, style)

def multi_card_widgets(cards, style):
    if len(cards) == 0:
        return [pass_label[style]]
    else:
        cards = main.symbolify_cards(cards)
        return list(map(lambda c: single_card_widget(c, style), cards))

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

def display_cards(cards, shift=0, style='op'):
    print(
        shift_card_widgets(
            merge_card_widgets(multi_card_widgets(cards, style)),
            shift
        )
    )

def display_table(me, op, played_hand, by):
    os.system('clear')

    display_cards(op, 30, 'op')
    display_cards(played_hand[1], 15, by)
    display_cards(me, 0, 'me')
            
if __name__ == '__main__':
    cards = main.parse_cards("bl22aa33jkq45690")
    print(display_cards(cards, 30, 'me'))
    
