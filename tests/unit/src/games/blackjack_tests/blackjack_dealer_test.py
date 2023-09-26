"""test blackjack dealer"""
# Date:	25 Sep 2023
# Revision History:
#	resultay | 25-09-23 | Initial version

import pytest
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.general.card import Card

@pytest.fixture()
def dealer() -> BlackjackDealer:
    """fixture returns dealer"""
    return BlackjackDealer()

def test_cannot_double_down(dealer: BlackjackDealer):
    """dealer cannot double down"""
    assert not dealer.can_double_down()

def test_can_hit(dealer: BlackjackDealer):
    """dealer can hit"""
    assert dealer.can_hit()

def test_cannot_hit(ace: Card, dealer: BlackjackDealer):
    """dealer cannot hit with face down card"""
    dealer.add_card(ace)
    assert dealer.can_hit()
    ace.flip()
    assert not dealer.can_hit()

def test_cannot_split(dealer: BlackjackDealer):
    """dealer cannot split"""
    assert not dealer.can_split()

can_stand_soft = [pytest.param(i, True) for i in range(18, 22)]
can_stand_hard = [pytest.param(i, False) for i in range(17, 22)]

@pytest.mark.parametrize(
    'points, soft',
    can_stand_soft + can_stand_hard
)
def test_can_stand(
    ace: Card,
    dealer: BlackjackDealer,
    non_ace: Card,
    points: int,
    soft: bool,
):
    """dealer can stand"""
    card = ace if soft else non_ace
    card.points = points
    dealer.add_card(card)
    dealer.add_card(Card(None, None))
    assert dealer.can_stand()

def test_cannot_stand_soft17(ace: Card, dealer: BlackjackDealer):
    """dealer cannot stand on soft 17"""
    ace.points = 17
    dealer.add_card(ace)
    dealer.add_card(Card(None, None))
    assert not dealer.can_stand()

def test_cannot_stand_16(ace: Card, dealer: BlackjackDealer):
    """dealer cannot stand on 16-"""
    dealer.add_card(ace)
    dealer.add_card(Card(None, None))
    for i in range(0, 17):
        ace.points = i
        assert not dealer.can_stand()

def test_cannot_surrender(dealer: BlackjackDealer):
    """dealer cannot surrender"""
    assert not dealer.can_surrender()

def test_flip(
    ace: Card,
    dealer: BlackjackDealer,
    non_ace: Card,
):
    """dealer flips last card"""
    dealer.add_card(ace)
    dealer.add_card(non_ace)
    dealer.flip()
    assert not non_ace.face_down
    assert ace.face_down

def test_sort_hand(
    ace: Card,
    dealer: BlackjackDealer,
    non_ace: Card,
):
    """flipped card is last"""
    dealer.add_card(ace)
    dealer.add_card(non_ace)
    assert dealer.hand[-1] == ace
    non_ace.flip()
    dealer.sort_hand()
    assert dealer.hand[-1] == non_ace
