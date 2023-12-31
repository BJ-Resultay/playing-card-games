"""module models blackjack hand"""
# Date:	13 Sep 2023
# Revision History:
#	resultay | 13-09-23 | Initial version

from __future__ import annotations
from src.general import Face
from src.general.card import Card

class BlackjackHand(list):
    """class models blackjack hand"""
    def __init__(self, iterable: list[Card] = None):
        """
        Args:
            iterable (list[Card], optional): cards already in hand
        """
        if iterable is not None:
            super().__init__(iterable)
        else:
            super().__init__()
        self.double = False
        """whether bet will be doubled if win"""

        self.end = False
        """whether hand accepts cards"""

    def __sum(self) -> int:
        """function sums total card points\n
        ignore face down crads

        Returns:
            int: sum of points
        """
        return sum(card.points if not card.face_down else 0 for card in self)

    def bust(self) -> bool:
        """function score is over 21

        Returns:
            bool: if hand bust
        """
        return self.score() > 21

    def face_values(self) -> None:
        """function returns face values of hand"""
        return [card.face_value() for card in self if not card.face_down]

    def score(self) -> int:
        """function adds up points\n
        calculates aces points

        Returns:
            int: score
        """
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
        """function checks if ace is 11

        Returns:
            bool: if hand is soft
        """
        if (any(card.face == Face.ACE for card in self)
            and self.__sum() == self.score()):
            return True
        return False

    def split(self) -> BlackjackHand:
        """function cuts hand in half

        Raises:
            IndexError: can only split hand of size 2

        Returns:
            BlackjackHand: new hand
        """
        if not len(self) == 2:
            raise IndexError('can only split hand of size 2')
        other = BlackjackHand()
        other.append(self.pop())
        return other
