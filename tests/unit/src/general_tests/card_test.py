"""test card"""
# Date:	15 Aug 2023
# Revision History:
#	resultay | 15-08-23 | Initial version

from src.constants import Face
from src.constants import Suit
from src.general import Card

def test_frozen():
    """trying to override face value raises an error"""
    card = Card(Face.ACE, Suit.SPADE)
    try:
        # cheater switching out the card
        card.face = Face.KING
    except AttributeError:
        assert True

def test_flip():
    """card flips over"""
    card = Card(Face.ACE, Suit.SPADE)
    assert card.face_down
    card.flip()
    assert not card.face_down

def test_face_value():
    """returns face value"""
    card = Card(Face.ACE, Suit.SPADE)
    assert card.face_value() == 'A\u2660'
