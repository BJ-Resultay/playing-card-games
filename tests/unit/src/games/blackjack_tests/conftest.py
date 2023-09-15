"""blackjack fixtures"""
# Date:	14 Sep 2023
# Revision History:
#	resultay | 14-09-23 | Initial version

import pytest
from src.constants import Face
from src.constants import Suit
from src.general.card import Card

@pytest.fixture()
def ace() -> Card:
    """fixture returns face up ace of spades"""
    card = Card(Face.ACE, Suit.SPADE, 11)
    card.flip()
    return card

@pytest.fixture()
def non_ace() -> Card:
    """fixture returns face up queen of hearts"""
    card = Card(Face.QUEEN, Suit.HEART, 10)
    card.flip()
    return card
