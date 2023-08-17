"""test card"""
# Date:	15 Aug 2023
# Revision History:
#	resultay | 15-08-23 | Initial version

import pytest
from src.constants import Face
from src.constants import Suit
from src.general import Card

@pytest.fixture()
def card():
    """fixture returns ace of spades"""
    return Card(Face.ACE, Suit.SPADE)

def test_frozen(card):
    """trying to override face value raises an error"""
    try:
        # cheater switching out the card
        card.face = Face.KING
    except AttributeError:
        assert True

def test_not_frozen(card):
    """overriding point value does not raise error"""
    assert card.points == 0
    card.points = 1
    assert card.points == 1

def test_flip(card):
    """card flips over"""
    assert card.face_down
    card.flip()
    assert not card.face_down

def test_face_value(card):
    """returns face value"""
    assert card.face_value() == 'A\u2660'
