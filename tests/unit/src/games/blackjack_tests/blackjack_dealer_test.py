"""test blackjack dealer"""
# Date:	25 Sep 2023
# Revision History:
#	resultay | 25-09-23 | Initial version

from pytest_mock import MockerFixture
import pytest
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.constants import BlackjackError
from src.general.card import Card

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

def test_turn(
    ace: Card,
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """dealer hits then stands"""
    mocker.patch.object(dealer, 'can_stand', side_effect = [False, True, True])
    mocker.patch.object(dealer, 'can_hit', return_value = True)
    mocker.patch.object(deck, 'draw', return_value = ace)
    hit = mocker.spy(dealer, 'hit')
    stand = mocker.spy(dealer, 'stand')

    ace.flip()
    dealer.add_card(ace)
    dealer.turn(deck)
    hit.assert_called_once_with(ace)
    stand.assert_called_once()
    assert not ace.face_down

def test_turn_error(
    ace: Card,
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """dealer has no moves"""
    mocker.patch.object(dealer, 'can_stand', return_value = False)
    mocker.patch.object(dealer, 'can_hit', return_value = False)

    ace.flip()
    dealer.add_card(ace)
    with pytest.raises(BlackjackError):
        dealer.turn(deck)
