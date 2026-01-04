"""test player"""
# Date:	20 Aug 2023
# Revision History:
#	resultay | 20-08-23 | Initial version

import pytest
from src.general import Face
from src.general import Suit
from src.general.card import Card
from src.general.player import (
    InsufficientAmount,
    NotNumeric,
    NotPositive,
    Player,
)

@pytest.fixture()
def player() -> Player:
    """fixture returns player"""
    return Player(name='René Lavand')

@pytest.fixture()
def card() -> Card:
    """fixture returns ace of spades"""
    return Card(Face.ACE, Suit.SPADE)

def test_add_card(player: Player, card: Card):
    """adds card to hand"""
    player.add_card(card)
    assert player.hand == [card]

def test_add_card_error(player: Player):
    """adding non card raises error"""
    with pytest.raises(AttributeError):
        player.add_card('not card')

def test_bet_chips(player: Player):
    """move chips to bet"""
    player.bet_chips(5)
    assert player.bet == 5.0
    assert player.chips == player.STARTING_CHIPS - 5.0

def test_bet_more_chips(player: Player):
    """bets accumulate"""
    player.bet_chips(5)
    player.bet_chips(5)
    assert player.bet == 10.0

def test_bet_chips_not_number(player: Player):
    """non number raises error"""
    with pytest.raises(NotNumeric):
        player.bet_chips('5')

def test_bet_negative_chips(player: Player):
    """negative number raises error"""
    with pytest.raises(NotPositive):
        player.bet_chips(-5)

def test_bet_too_many_chips(player: Player):
    """going over raises error"""
    with pytest.raises(InsufficientAmount):
        player.bet_chips(player.STARTING_CHIPS + 1)

def test_bet_win(player: Player):
    """winning bet increases money"""
    player.bet_chips(5)
    player.bet_win()
    assert player.chips == player.STARTING_CHIPS + 5.0

def test_bet_win_not_number(player: Player):
    """non number raises error"""
    with pytest.raises(AttributeError):
        player.bet_win('car')

def test_bet_win_lose_money(player: Player):
    """win but lose money"""
    with pytest.raises(AttributeError):
        player.bet_win(-1)

def test_increase_stat(player: Player):
    """stat increases by 1"""
    player.increase_stat('new_stat')
    assert player.stats['new_stat'] == 1

def test_increase_invalid_stat(player: Player):
    """invalid stat raises error"""
    with pytest.raises(AttributeError):
        player.increase_stat(1)

def test_sort_hand(player: Player, card: Card):
    """hand sorts cards"""
    card2 = Card(Face.KING, Suit.CLUB)
    card3 = Card('face', 'suit')
    player.add_card(card) # 39
    player.add_card(card2) # 12
    player.add_card(card3) # math.inf
    player.sort_hand()
    assert player.hand == [card2, card, card3]
