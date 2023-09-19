"""test blackjack deck"""
# Date:	19 Sep 2023
# Revision History:
#	resultay | 19-09-23 | Initial version

import pytest
from src.constants import Face
from src.games.blackjack.blackjack_deck import BlackjackDeck

@pytest.fixture()
def deck():
    """fixture returns blackjack deck"""
    return BlackjackDeck()

def test_card_points(deck: BlackjackDeck):
    """points are correct"""
    for face in Face:
        card = deck.deal()
        assert card.face == face
        assert card.points == deck.FACE_TO_POINTS[face]
