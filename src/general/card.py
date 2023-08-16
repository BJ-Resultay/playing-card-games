"""module models playing card"""
# Date:	15 Aug 2023
# Revision History:
#	resultay | 15-08-23 | Initial version

import constants

class Card():
    """class models playing card"""
    UNKNOWN = 'unknown'
    _frozen = False

    def __init__(
        self,
        face: constants.Face,
        suit: constants.Suit,
        points = 0,
    ) -> None:
        self.face = face
        self.face_down = True # default hidden
        self.points = points
        self.suit = suit
        self._frozen = True

    def __setattr__(self, attr, value) -> None:
        if self._frozen and attr in ('face', 'suit'):
            raise AttributeError('msg')
        return super().__setattr__(attr, value)

    def flip(self) -> bool:
        """function flips card over"""
        self.face_down = not self.face_down
        return self.face_down

    def face_value(self) -> str:
        """function returns face value"""
        return self.face.value + self.suit.value
