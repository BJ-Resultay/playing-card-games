"""module models playing card"""
# Date:	15 Aug 2023
# Revision History:
#	resultay | 15-08-23 | Initial version

from __future__ import annotations
from src.constants import Face
from src.constants import Suit

class Card():
    """class models playing card"""
    UNKNOWN = 'unknown'
    _frozen = False

    def __init__(
        self,
        face: Face,
        suit: Suit,
        points = 0,
    ) -> None:
        self.face = face
        self.face_down = True # default hidden
        self.points = points
        self.suit = suit
        self._frozen = True

    def __eq__(self, other: Card) -> bool:
        if not isinstance(other, Card):
            return False
        return self.face == other.face and self.suit == other.suit

    def __setattr__(self, attr, value) -> None:
        if self._frozen and attr in ('face', 'suit'):
            raise AttributeError('faces and suits of cards are frozen')
        return super().__setattr__(attr, value)

    def face_value(self) -> str:
        """function returns face value"""
        return self.face.value + self.suit.value

    def flip(self) -> None:
        """function flips card over"""
        self.face_down = not self.face_down
