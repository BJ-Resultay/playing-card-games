"""module models blackjack hand"""
# Date:	13 Sep 2023
# Revision History:
#	resultay | 13-09-23 | Initial version

from __future__ import annotations
from collections.abc import Iterable
from src.general import Face

class BlackjackHand(list):
    """class models blackjack hand"""
    def __init__(self, iterable: Iterable = None):
        if iterable is not None:
            super().__init__(iterable)
        else:
            super().__init__()
        self.double = False
        """whether bet will be doubled if wim"""

        self.end = False
        """whether hand accepts cards"""

    def __sum(self) -> int:
        """function sums total card points"""
        return sum(card.points if not card.face_down else 0 for card in self)

    def bust(self) -> bool:
        """function score is over 21"""
        return self.score() > 21

    def face_values(self) -> None:
        """function returns face values of hand"""
        return [card.face_value() for card in self if not card.face_down]

    def score(self) -> int:
        """function adds up points"""
        score = self.__sum()
        if score <= 21:
            return score

        # aces are 11 or 1
        num_aces = len([card for card in self if card.face == Face.ACE])
        for _ in range(num_aces):
            score -= 10
            if score <= 21:
                return score
        return score

    def soft(self) -> bool:
        """function checks if ace is 11"""
        if (any(card.face == Face.ACE for card in self)
            and self.__sum() == self.score()):
            return True
        return False

    def split(self) -> BlackjackHand:
        """function cuts hand in half"""
        if not len(self) == 2:
            raise IndexError('can only split hand of size 2')
        other = BlackjackHand()
        other.append(self.pop())
        return other
