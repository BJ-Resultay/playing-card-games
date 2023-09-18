"""test blackjack player"""
# Date:	14 Sep 2023
# Revision History:
#	resultay | 14-09-23 | Initial version

import pytest
from src.constants import Face
from src.constants.blackjack import BLACKJACK
from src.constants.blackjack import BlackjackError
from src.games.blackjack.blackjack_player import BlackjackPlayer
from src.general.card import Card

@pytest.fixture()
def player() -> BlackjackPlayer:
    """fixture returns blackjack player"""
    return BlackjackPlayer('Bill Malone')

class TestDoubleDown():
    """test double down related functions"""
    def should_double_down(
        self,
        card: Card,
        mask: list[int],
    ) -> None:
        """test_should_double_down helper"""
        player = BlackjackPlayer('new')
        player.hit(card)
        for i in range(2, 12):
            if i in mask:
                assert player.should_double_down(i)
            else:
                assert not player.should_double_down(i)

    @pytest.mark.parametrize(
        'points, mask',
        [
            (13, [5, 6]),
            (14, [5, 6]),
            (15, range(4, 7)),
            (16, range(4, 7)),
            (17, range(3, 7)),
            (18, range(2, 7)),
            (19, [6]),
            (20, []),
            (21, []),
        ]
    )
    def test_should_double_down_soft(
        self,
        ace: Card,
        mask: list[int],
        points: int,
    ):
        """player should double down with soft hand"""
        # Soft 19 doubles against dealer 6
        # Soft 18 doubles against dealer 2 through 6
        # Soft 17 doubles against dealer 3 through 6
        # Soft 16 doubles against dealer 4 through 6
        # Soft 15 doubles against dealer 4 through 6
        # Soft 14 doubles against dealer 5 through 6
        # Soft 13 doubles against dealer 5 through 6
        ace.points = points
        self.should_double_down(ace, mask)

    should_not_double_down_hard_param = [
        pytest.param(i, [])
        for i in range(9, 22)
        if i not in range(2, 12)
    ]

    @pytest.mark.parametrize(
        'points, mask',
        [
            (10, range(2, 10)),
            (11, range(2, 12)),
            (9, range(3, 7)),
        ] + should_not_double_down_hard_param
    )
    def test_should_double_down_hard(
        self,
        mask: list[int],
        non_ace: Card,
        points: int,
    ):
        """player should double down with hard hand"""
        # Hard 11 always doubles.
        # Hard 10 doubles against dealer 2 through 9
        # Hard 9 doubles against dealer 3 through 6
        non_ace.points = points
        self.should_double_down(non_ace, mask)

    def test_can_double_down_true(
        self,
        ace: Card,
        player: BlackjackPlayer,
    ):
        """player can double down"""
        player.hit(ace)
        player.hit(ace)
        assert player.can_double_down()

    def test_can_double_down_false(
        self,
        ace: Card,
        player: BlackjackPlayer,
    ):
        """player cannot double down"""
        assert not player.can_double_down()
        player.hit(ace)
        player.hit(ace)
        player.bet_chips(player.STARTING_CHIPS)
        assert not player.can_double_down()

    def test_double_down(
        self,
        ace: Card,
        non_ace: Card,
        player: BlackjackPlayer,
    ):
        """player doubled down"""
        player.bet_chips(5)
        player.hit(ace)
        player.hit(ace)
        player.double_down(non_ace)
        assert non_ace in player.hand
        assert player.hand.double
        assert player.hand.end
        assert player.chips == player.STARTING_CHIPS - 5 * 2

    def test_double_down_error(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot double down raises error"""
        with pytest.raises(BlackjackError):
            player.double_down(ace)

class TestSplit():
    """test split related functions"""
    should_not_split_param = [
        pytest.param(face, [])
        for face in [Face.TEN, Face.FIVE, Face.JACK, Face.KING, Face.QUEEN]
    ]

    @pytest.mark.parametrize(
        'face, mask',
        [
            (Face.ACE, range(2, 12)),
            (Face.EIGHT, range(2, 12)),
            (Face.FOUR, [5, 6]),
            (Face.NINE, list(range(2, 7)) + [8, 9]),
            (Face.SEVEN, range(2, 8)),
            (Face.SIX, range(2, 7)),
            (Face.THREE, range(2, 8)),
            (Face.TWO, range(2, 8)),
        ] + should_not_split_param
    )
    def test_should_split(
        self,
        face: Face,
        mask: list[int],
        player: BlackjackPlayer,
    ):
        """player should split"""
        # Always split As
        # 9s splits against dealer 2 through 9, not 7
        # Always split 8s
        # 7s splits against dealer 2 through 7
        # 6s splits against dealer 2 through 6
        # 4s splits against dealer 5 and 6
        # 3s splits against dealer 2 through 7
        # 2s splits against dealer 2 through 7
        card = Card(face, None)
        player.hit(card)
        player.hit(card)
        for i in range(2, 12):
            if i in mask:
                assert player.should_split(i)
            else:
                assert not player.should_split(i)

    def test_can_split_true(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player can split"""
        player.hit(ace)
        player.hit(ace)
        assert player.can_split()

    def test_can_split_not_two_false(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player can not split not 2 cards"""
        player.hit(ace)
        assert not player.can_split()
        player.hit(ace)
        player.hit(ace)
        assert not player.can_split()

    def test_can_split_different_cards(
        self,
        ace: Card,
        non_ace: Card,
        player: BlackjackPlayer,
    ):
        """player cannot split different cards"""
        player.hit(ace)
        player.hit(non_ace)
        assert not player.can_split()

    def test_can_split_too_poor(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot split without bet"""
        player.hit(ace)
        player.hit(ace)
        player.bet_chips(player.STARTING_CHIPS)
        assert not player.can_split()

    def test_split(
        self,
        ace: Card,
        non_ace: Card,
        player: BlackjackPlayer,
    ):
        """player splits"""
        player.bet_chips(5)
        player.hit(ace)
        player.hit(ace)
        player.split(non_ace, non_ace)
        assert len(player.hands) == 2
        assert ace in player.hand
        assert non_ace in player.hand
        assert ace in player.hands[-1]
        assert non_ace in player.hands[-1]
        assert player.chips == player.STARTING_CHIPS - 5 * 2

    def test_split_error(self, player: BlackjackPlayer):
        """player splits with too few cards raises error"""
        with pytest.raises(BlackjackError):
            player.split(None, None)

class TestStand():
    """test stand related functions"""
    def test_can_stand_true(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player can stand"""
        player.hit(ace)
        player.hit(ace)
        assert player.can_stand()

    def test_can_stand_false(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot stand"""
        assert not player.can_stand()
        player.hit(ace)
        assert not player.can_stand()

    def test_should_stand18(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player should not stand with soft 18 against dealer 9 through Ace"""
        player.hit(ace)
        ace.points = 18
        for i in range(2, 9):
            assert player.should_stand(i)
        for i in range(9, 12):
            assert not player.should_stand(i)

    def test_should_stand(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player should stand with 17+"""
        player.hit(non_ace)
        for i in range(17, 22):
            non_ace.points = i
            for j in range(9, 12):
                assert player.should_stand(j)

    def test_should_not_stand(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player should not stand with 16-"""
        player.hit(non_ace)
        for i in range(4, 17):
            non_ace.points = i
            for j in range(9, 12):
                assert not player.should_stand(j)

    def test_stand(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player stands"""
        player.hit(non_ace)
        player.hit(non_ace)
        player.stand()
        assert player.hand.end

    def test_stand_error(self, player: BlackjackPlayer):
        """player stand with too few cards raises error"""
        with pytest.raises(BlackjackError):
            player.stand()

class TestSurrender():
    """test surrender related functions"""
    def test_can_surrender_true(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player can surrender"""
        player.hit(ace)
        player.hit(ace)
        assert player.can_surrender()

    def test_can_surrender_hit(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot surrender after double down or hit"""
        player.hit(ace)
        player.hit(ace)
        player.hit(ace)
        assert not player.can_surrender()

    def test_can_surrender_split(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot surrender after split"""
        player.hit(ace)
        player.hit(ace)
        player.hands.append('some hand')
        assert not player.can_surrender()

    def test_should_surrender15(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player should surrender with 15 against dealer 10"""
        player.hit(non_ace)
        non_ace.points = 15
        assert player.should_surrender(10)
        for i in range(2, 12):
            if i == 10:
                continue
            assert not player.should_surrender(i)

    def test_should_surrender16(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player should surrender with 15 against dealer 9 through Ace"""
        player.hit(non_ace)
        non_ace.points = 16
        for i in range(9, 12):
            assert player.should_surrender(10)
        for i in range(2, 9):
            assert not player.should_surrender(i)

    def test_should_not_surrender(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player should not surrender otherwise"""
        player.hit(non_ace)
        for i in range(4, 22):
            if i in [15, 16]:
                continue
            assert not player.should_surrender(i)

    def test_surrender(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player surrenders"""
        player.bet_chips(5)
        player.hit(non_ace)
        player.hit(non_ace)
        player.surrender()
        assert player.chips == player.STARTING_CHIPS - 5.0 / 2
        assert player.hand.end

def test_blackjack_true(
    ace: Card,
    non_ace: Card,
    player: BlackjackPlayer,
):
    """player hit blackjack"""
    player.hit(ace)
    player.hit(non_ace)
    assert player.blackjack()

def test_blackjack_false(
    ace: Card,
    non_ace: Card,
    player: BlackjackPlayer,
):
    """player did not hit blackjack"""
    player.hit(ace)
    player.hit(non_ace)
    player.hit(non_ace)
    assert not player.blackjack()

def test_blackjack_unnatural(
    ace: Card,
    non_ace: Card,
    player: BlackjackPlayer,
):
    """player hit blackjack after split"""
    player.hit(ace)
    player.hit(non_ace)
    player.hands.append('some hand')
    assert not player.blackjack()

def test_can_hit_true(non_ace: Card, player: BlackjackPlayer):
    """player can hit"""
    player.hit(non_ace)
    player.hit(non_ace)
    assert player.can_hit()

def test_can_hit_false(non_ace: Card, player: BlackjackPlayer):
    """player can hit"""
    player.hit(non_ace)
    player.hit(non_ace)
    player.hit(non_ace)
    assert not player.can_hit()

def test_discard_cards(ace: Card, player: BlackjackPlayer):
    """player discards cards"""
    player.hit(ace)
    player.hands.append('some hand')
    player.discard_cards()
    assert len(player.hand) == 0
    assert len(player.hands) == 1

def test_hit(non_ace: Card, player: BlackjackPlayer):
    """player hits"""
    player.hit(non_ace)
    player.hit(non_ace)
    assert not player.hand.end
    player.hit(non_ace)
    assert player.hand.end

def test_hit_error(non_ace: Card, player: BlackjackPlayer):
    """player cannot hit raises error"""
    player.hit(non_ace)
    player.hit(non_ace)
    player.hit(non_ace)
    with pytest.raises(BlackjackError):
        player.hit(non_ace)

def test_increase_stat(player: BlackjackPlayer):
    """stat increases by 1"""
    player.increase_stat('new_stat')
    assert player.stats[BLACKJACK]['new_stat'] == 1

def test_increase_invalid_stat(player: BlackjackPlayer):
    """invalid stat raises error"""
    with pytest.raises(AttributeError):
        player.increase_stat(1)
