"""test blackjack deck"""
# Date:	19 Sep 2023
# Revision History:
#	resultay | 19-09-23 | Initial version

from src.general import Face
from src.games.blackjack.blackjack_deck import BlackjackDeck

def test_card_points(deck: BlackjackDeck):
    """points are correct"""
    for face in Face:
        card = deck.deal()
        assert card.face == face
        assert card.points == deck.FACE_TO_POINTS[face]

def test_draw(deck: BlackjackDeck):
    """player draws card"""
    assert deck.face_down
    card = deck.draw()
    assert card.face_value() == 'A\u2665'
    assert not card.face_down

def test_draw_flip(deck: BlackjackDeck):
    """player flips deck face down"""
    deck.flip()
    assert not deck.face_down
    card = deck.draw()
    assert deck.face_down
    assert not card.face_down

    deck.draw()
    assert deck.face_down
