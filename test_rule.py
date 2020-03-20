import unittest

from rule import parse_cards, cards_in, cards_sub
from rule import HandKind, get_hands
from rule import cmp_hands

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

    def test_get_hand_double(self):
        all_cards = parse_cards("333444456678900A22")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.DOUBLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("33"),
                parse_cards("44"),
                parse_cards("66"),
                parse_cards("00"),
                parse_cards("22"),
            ]
        )

    def test_get_hand_double_straight(self):
        all_cards = parse_cards("3334444556678900A22")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.DOUBLE_STRAIGHT, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("334455"),
                parse_cards("445566"),
                parse_cards("33445566"),
            ]
        )

    def test_get_hand_triple(self):
        all_cards = parse_cards("33344445")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.TRIPLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("333"),
                parse_cards("444"),
            ]
        )

    def test_get_hand_triple_plus_single(self):
        all_cards = parse_cards("33344445")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.TRIPLE_PLUS_SINGLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("3334"),
                parse_cards("3335"),
                parse_cards("4443"),
                parse_cards("4445"),
            ]
        )

    def test_get_hand_triple_plus_double(self):
        all_cards = parse_cards("33344445")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.TRIPLE_PLUS_DOUBLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("33344"),
                parse_cards("44433"),
            ]
        )

    def test_get_hand_plane(self):
        all_cards = parse_cards("3334444555667")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.PLANE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("333444"),
                parse_cards("444555"),
                parse_cards("333444555"),
            ]
        )

    def test_get_hand_plane_plus_single(self):
        all_cards = parse_cards("3334444555667")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.PLANE_PLUS_SINGLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("33344445"),
                parse_cards("33344446"),
                parse_cards("33344447"),
                parse_cards("33344456"),
                parse_cards("33344457"),
                parse_cards("33344467"),
                parse_cards("44455534"),
                parse_cards("44455536"),
                parse_cards("44455537"),
                parse_cards("44455546"),
                parse_cards("44455547"),
                parse_cards("44455567"),
                parse_cards("333444555467"),
            ]
        )

    def test_get_hand_plane_plus_double(self):
        all_cards = parse_cards("3334444555667")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.PLANE_PLUS_DOUBLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("3334445566"),
                parse_cards("4445553366"),
            ]
        )

    def test_get_hand_bomb(self):
        all_cards = parse_cards("3334444555667")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.BOMB, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("4444"),
            ]
        )
        
    def test_get_hand_rocket(self):
        all_cards = parse_cards("3334444555667LB")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.ROCKET, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("LB"),
            ]
        )

    def test_get_hand_quadruple_plus_single(self):
        all_cards = parse_cards("3334444555667")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.QUADRUPLE_PLUS_SINGLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("444435"),
                parse_cards("444436"),
                parse_cards("444437"),
                parse_cards("444456"),
                parse_cards("444457"),
                parse_cards("444467"),
            ]
        )

    def test_get_hand_quadruple_plus_double(self):
        all_cards = parse_cards("3334444555667")
        all_hand_cards = [hand_cards for (_, hand_cards), _ in get_hands(HandKind.QUADRUPLE_PLUS_DOUBLE, all_cards)]

        self.assertCountEqual(
            all_hand_cards,
            [
                parse_cards("44443355"),
                parse_cards("44443366"),
                parse_cards("44445566"),
            ]
        )


    def test_cmp_hands(self):
        self.assertTrue(cmp_hands(
            (HandKind.SINGLE, parse_cards("2")),
            (HandKind.SINGLE, parse_cards("A")),
        ))
        
        self.assertTrue(cmp_hands(
            (HandKind.STRAIGHT, parse_cards("0JQKA")),
            (HandKind.STRAIGHT, parse_cards("90JQK")),
        ))
        self.assertFalse(cmp_hands(
            (HandKind.STRAIGHT, parse_cards("90JQKA")),
            (HandKind.STRAIGHT, parse_cards("90JQK")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.DOUBLE, parse_cards("22")),
            (HandKind.DOUBLE, parse_cards("AA")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.DOUBLE_STRAIGHT, parse_cards("00JJQQ")),
            (HandKind.DOUBLE_STRAIGHT, parse_cards("9900JJ")),
        ))
        self.assertFalse(cmp_hands(
            (HandKind.DOUBLE_STRAIGHT, parse_cards("00JJQQKK")),
            (HandKind.DOUBLE_STRAIGHT, parse_cards("9900JJ")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.TRIPLE, parse_cards("222")),
            (HandKind.TRIPLE, parse_cards("000")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.TRIPLE_PLUS_SINGLE, parse_cards("2223")),
            (HandKind.TRIPLE_PLUS_SINGLE, parse_cards("AAAB")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.TRIPLE_PLUS_DOUBLE, parse_cards("222AA")),
            (HandKind.TRIPLE_PLUS_DOUBLE, parse_cards("AAA22")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.PLANE, parse_cards("KKKAAA")),
            (HandKind.PLANE, parse_cards("QQQKKK")),
        ))
        self.assertFalse(cmp_hands(
            (HandKind.PLANE, parse_cards("QQQKKKAAA")),
            (HandKind.PLANE, parse_cards("QQQKKK")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.PLANE_PLUS_SINGLE, parse_cards("KKKAAA34")),
            (HandKind.PLANE_PLUS_SINGLE, parse_cards("QQQKKKA2")),
        ))
        self.assertFalse(cmp_hands(
            (HandKind.PLANE_PLUS_SINGLE, parse_cards("QQQKKKAAA345")),
            (HandKind.PLANE_PLUS_SINGLE, parse_cards("QQQKKKA2")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.PLANE_PLUS_DOUBLE, parse_cards("KKKAAA3344")),
            (HandKind.PLANE_PLUS_DOUBLE, parse_cards("QQQKKKAA22")),
        ))
        self.assertFalse(cmp_hands(
            (HandKind.PLANE_PLUS_DOUBLE, parse_cards("QQQKKKAAA334455")),
            (HandKind.PLANE_PLUS_DOUBLE, parse_cards("QQQKKKAA22")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.BOMB, parse_cards("2222")),
            (HandKind.BOMB, parse_cards("AAAA")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.QUADRUPLE_PLUS_SINGLE, parse_cards("222234")),
            (HandKind.QUADRUPLE_PLUS_SINGLE, parse_cards("AAAALB")),
        ))

        self.assertTrue(cmp_hands(
            (HandKind.QUADRUPLE_PLUS_DOUBLE, parse_cards("222233")),
            (HandKind.QUADRUPLE_PLUS_DOUBLE, parse_cards("AAAA22")),
        ))


if __name__ == '__main__':
    unittest.main()
