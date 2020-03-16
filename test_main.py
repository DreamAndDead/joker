import unittest

from main import parse_cards, cards_in, cards_sub
from main import HandKind, get_hands

class TestMain(unittest.TestCase):
    def test_list_equal_no_matter_order(self):
        self.assertCountEqual(
            [1, 2, 3, 1],
            [1, 3, 2, 1],
            [3, 1, 1, 2],
        )
    
    def test_cards_in(self):
        self.assertTrue(
            cards_in(
                parse_cards("3344"),
                parse_cards("334455")
            )
        )
        
        self.assertFalse(
            cards_in(
                parse_cards("33445"),
                parse_cards("34455")
            )
        )

    def test_cards_sub(self):
        self.assertCountEqual(
            cards_sub(
                parse_cards(""),
                parse_cards("")
            ),
            parse_cards("")
        )

        self.assertCountEqual(
            cards_sub(
                parse_cards("34567JQK"),
                parse_cards("46JK")
            ),
            parse_cards("357Q")
        )

        self.assertCountEqual(
            cards_sub(
                parse_cards("33445566"),
                parse_cards("345")
            ),
            parse_cards("34566")
        )


    def test_get_hand_pass(self):
        all_cards = parse_cards("3452")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.PASS, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards(""),
            ]
        )

    def test_get_hand_single(self):
        all_cards = parse_cards("3452")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.SINGLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("3"),
                parse_cards("4"),
                parse_cards("5"),
                parse_cards("2"),
            ]
        )

    def test_get_hand_straight(self):
        all_cards = parse_cards("34567890A2")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.STRAIGHT, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("34567"),
                parse_cards("345678"),
                parse_cards("3456789"),
                parse_cards("34567890"),
                parse_cards("45678"),
                parse_cards("456789"),
                parse_cards("4567890"),
                parse_cards("56789"),
                parse_cards("567890"),
                parse_cards("67890"),
            ]
        )



if __name__ == '__main__':
    unittest.main()
