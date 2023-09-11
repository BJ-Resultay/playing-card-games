"""test card"""
# Date:	15 Aug 2023
# Revision History:
#	resultay | 15-08-23 | Initial version

import pytest
from src.constants import Face
from src.constants import Suit
from src.general.card import Card

@pytest.fixture()
def card() -> Card:
    """fixture returns ace of spades"""
    return Card(Face.ACE, Suit.SPADE)

def test_equality(card: Card):
    """card instance equals a separate instance"""
    assert Card(Face.ACE, Suit.SPADE, 1) == card # points = 0

def test_equality_not_card(card: Card):
    """card instance does not equal not card"""
    assert not card == 'not card'

def test_frozen(card: Card):
    """overriding face value raises an error"""
    with pytest.raises(AttributeError):
        # cheater switching out the card
        card.face = Face.KING

def test_not_frozen(card: Card):
    """overriding point value does not raise error"""
    assert card.points == 0
    card.points = 1
    assert card.points == 1

def test_flip(card: Card):
    """card flips over"""
    assert card.face_down
    card.flip()
    assert not card.face_down

def test_face_value(card: Card):
    """returns face value"""
    assert card.face_value() == 'A\u2660'
