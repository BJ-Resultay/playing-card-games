"""module models blackjack deck"""
# Date:	28 Aug 2023
# Revision History:
#	resultay | 28-08-23 | Initial version

from logging import getLogger
from src.general import Face
from src.general.deck import Deck

LOGGER = getLogger(__name__)

class BlackjackDeck(Deck):
    """class models blackjack deck"""
    FACE_TO_POINTS = {
        Face.ACE: 11, # or 1
        Face.TWO: 2,
        Face.THREE: 3,
        Face.FOUR: 4,
        Face.FIVE: 5,
        Face.SIX: 6,
        Face.SEVEN: 7,
        Face.EIGHT: 8,
        Face.NINE: 9,
        Face.TEN: 10,
        Face.JACK: 10,
        Face.QUEEN: 10,
        Face.KING: 10
    }

    def __init__(self) -> None:
        super().__init__()
        self.logger = LOGGER

        for card in self.order:
            card.points = self.FACE_TO_POINTS[card.face]
