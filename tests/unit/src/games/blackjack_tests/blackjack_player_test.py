"""test blackjack player"""
# Date:	14 Sep 2023
# Revision History:
#	resultay | 14-09-23 | Initial version

import pytest
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.blackjack_player import BlackjackPlayer
from src.games.blackjack.constants import BLACKJACK, BlackjackError
from src.general.card import Card

@pytest.fixture()
def player() -> BlackjackPlayer:
    """fixture returns blackjack player"""
    return BlackjackPlayer('Bill Malone')

class TestDoubleDown():
    """test double down related functions"""
    def test_can_double_down_true(
        self,
        ace: Card,
        player: BlackjackPlayer,
    ):
        """player can double down"""
        player.add_card(ace)
        player.add_card(ace)
        assert player.can_double_down()

    def test_can_double_down_false(
        self,
        ace: Card,
        player: BlackjackPlayer,
    ):
        """player cannot double down"""
        assert not player.can_double_down()
        player.add_card(ace)
        player.add_card(ace)
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
        player.add_card(ace)
        player.add_card(ace)
        player.double_down(non_ace)
        assert non_ace in player.hand
        assert player.hand.double
        assert player.hand.end
        assert player.chips == player.STARTING_CHIPS - 5 * 2

    def test_double_down_bust(
        self,
        non_ace: Card,
        player: BlackjackPlayer,
    ):
        """player doubled down and bust"""
        player.bet_chips(5)
        player.add_card(non_ace)
        player.add_card(non_ace)
        player.double_down(non_ace)
        assert player.hand.bust()

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
    def test_can_split_true(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player can split"""
        player.add_card(ace)
        player.add_card(ace)
        assert player.can_split()

    def test_can_split_not_two_false(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player can not split not 2 cards"""
        player.add_card(ace)
        assert not player.can_split()
        player.add_card(ace)
        player.add_card(ace)
        assert not player.can_split()

    def test_can_split_different_cards(
        self,
        ace: Card,
        non_ace: Card,
        player: BlackjackPlayer,
    ):
        """player cannot split different cards"""
        player.add_card(ace)
        player.add_card(non_ace)
        assert not player.can_split()

    def test_can_split_too_poor(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot split without bet"""
        player.add_card(ace)
        player.add_card(ace)
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
        player.add_card(ace)
        player.add_card(ace)
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
        player.add_card(ace)
        player.add_card(ace)
        assert player.can_stand()

    def test_can_stand_false(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot stand"""
        assert not player.can_stand()
        player.add_card(ace)
        assert not player.can_stand()

    def test_stand(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player stands"""
        player.add_card(non_ace)
        player.add_card(non_ace)
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
        player.add_card(ace)
        player.add_card(ace)
        assert player.can_surrender()

    def test_can_surrender_hit(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot surrender after double down or hit"""
        player.add_card(ace)
        player.add_card(ace)
        player.add_card(ace)
        assert not player.can_surrender()

    def test_can_surrender_split(
        self,
        ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot surrender after split"""
        player.add_card(ace)
        player.add_card(ace)
        player.hands.append('some hand')
        assert not player.can_surrender()

    def test_surrender(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player surrenders"""
        player.bet_chips(5)
        player.add_card(non_ace)
        player.add_card(non_ace)
        player.surrender()
        assert player.chips == player.STARTING_CHIPS - 5.0 / 2
        assert player.hand.end

    def test_surrender_error(self, player: BlackjackPlayer):
        """player surrenders with too few cards"""
        with pytest.raises(BlackjackError):
            player.surrender()

class TestHit():
    """test hit related functions"""
    def test_can_hit_true(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player can hit"""
        player.hit(non_ace)
        player.hit(non_ace)
        assert player.can_hit()

    def test_can_hit_false(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player can hit"""
        player.hit(non_ace)
        player.hit(non_ace)
        player.hit(non_ace)
        assert not player.can_hit()

    def test_hit(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player hits"""
        player.hit(non_ace)
        player.hit(non_ace)
        assert not player.hand.end
        player.hit(non_ace)
        assert player.hand.end

    def test_hit_error(
        self,
        non_ace: Card,
        player: BlackjackPlayer
    ):
        """player cannot hit raises error"""
        player.hit(non_ace)
        player.hit(non_ace)
        player.hit(non_ace)
        with pytest.raises(BlackjackError):
            player.hit(non_ace)

def test_blackjack_true(
    ace: Card,
    non_ace: Card,
    player: BlackjackPlayer,
):
    """player hit blackjack"""
    player.add_card(ace)
    player.add_card(non_ace)
    assert player.blackjack()

def test_blackjack_false(
    ace: Card,
    non_ace: Card,
    player: BlackjackPlayer,
):
    """player did not hit blackjack"""
    player.add_card(ace)
    player.add_card(non_ace)
    player.add_card(non_ace)
    assert not player.blackjack()

def test_blackjack_unnatural(
    ace: Card,
    non_ace: Card,
    player: BlackjackPlayer,
):
    """player hit blackjack after split"""
    player.add_card(ace)
    player.add_card(non_ace)
    player.hands.append('some hand')
    assert not player.blackjack()

def test_discard_cards(ace: Card, player: BlackjackPlayer):
    """player discards cards"""
    player.add_card(ace)
    player.hands.append('some hand')
    player.discard_cards()
    assert len(player.hand) == 0
    assert len(player.hands) == 1

def test_increase_stat(player: BlackjackPlayer):
    """stat increases by 1"""
    player.increase_stat('new_stat')
    assert player.stats[BLACKJACK]['new_stat'] == 1

def test_increase_invalid_stat(player: BlackjackPlayer):
    """invalid stat raises error"""
    with pytest.raises(AttributeError):
        player.increase_stat(1)
