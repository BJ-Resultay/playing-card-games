"""module models blackjack player ai"""
# Date:	28 Sep 2023
# Revision History:
#	resultay | 28-09-23 | Initial version

from logging import getLogger
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.blackjack_player import BlackjackPlayer
from src.general import Face

LOGGER = getLogger(__name__)

class BlackjackBot(BlackjackPlayer):
    """class models blackjack player ai"""
    def __init__(self, name: str):
        """
        Args:
            name (str): distinguish players in human readable format
        """
        super().__init__(name)
        self.logger = LOGGER

    def should_double_down(self, dealer_score: int) -> bool:
        """function checks whether to double down

        Args:
            dealer_score (int): face up card

        Returns:
            bool: if bot should double down
        """
        # Soft 19 doubles against dealer 6
        # Soft 18 doubles against dealer 2 through 6
        # Soft 17 doubles against dealer 3 through 6
        # Soft 16 doubles against dealer 4 through 6
        # Soft 15 doubles against dealer 4 through 6
        # Soft 14 doubles against dealer 5 through 6
        # Soft 13 doubles against dealer 5 through 6
        # Hard 11 always doubles.
        # Hard 10 doubles against dealer 2 through 9
        # Hard 9 doubles against dealer 3 through 6
        score = self.hand.score()
        soft_vs_dealer = {
            13: [5, 6],
            14: [5, 6],
            15: range(4, 7),
            16: range(4, 7),
            17: range(3, 7),
            18: range(2, 7),
            19: [6],
        }
        hard_vs_dealer = {
            10: range(2, 10),
            11: range(2, 12),
            9: range(3, 7),
        }
        if self.hand.soft():
            if dealer_score in soft_vs_dealer.get(score, []):
                return True
        else:
            if dealer_score in hard_vs_dealer.get(score, []):
                return True
        return False

    def should_split(self, dealer_score: int) -> bool:
        """function checks whether to split

        Args:
            dealer_score (int): face up card

        Returns:
            bool: if bot should split
        """
        # Always split As
        # 9s splits against dealer 2 through 9, not 7
        # Always split 8s
        # 7s splits against dealer 2 through 7
        # 6s splits against dealer 2 through 6
        # 4s splits against dealer 5 and 6
        # 3s splits against dealer 2 through 7
        # 2s splits against dealer 2 through 7
        face = self.hand[0].face
        two_seven = range(2, 8)
        two_six = list(range(2, 7))
        face_vs_dealer = {
            Face.ACE: range(2, 12),
            Face.EIGHT: range(2, 12),
            Face.FOUR: [5, 6],
            Face.NINE: list(two_six) + [8, 9],
            Face.SEVEN: two_seven,
            Face.SIX: two_six,
            Face.THREE: two_seven,
            Face.TWO: two_seven,
        }
        if dealer_score in face_vs_dealer.get(face, []):
            return True
        return False

    def should_stand(self, dealer_score: int) -> bool:
        """function checks whether to stand

        Args:
            dealer_score (int): face up card

        Returns:
            bool: if bot should stand
        """
        # Soft 18 hits against dealer 9 through Ace if not double
        # 17+ always stands
        score = self.hand.score()
        if (self.hand.soft()
            and score == 18
            and dealer_score in range(9, 12)):
            return False
        if score >= 17:
            return True
        return False

    def should_surrender(self, dealer_score: int) -> bool:
        """function checks whether to surrender

        Args:
            dealer_score (int): face up card

        Returns:
            bool: if bot should surrender
        """
        # 16 surrenders against dealer 9 through Ace
        # 15 surrenders against dealer 10
        score = self.hand.score()
        if score == 16 and dealer_score in [9, 10, 11]:
            return True
        if score == 15 and dealer_score == 10:
            return True
        return False

    def turn(self, deck: BlackjackDeck):
        """function decides bot's decisions for their turn

        Args:
            deck (BlackjackDeck): deck bot draws from
        """
        # https://www.youtube.com/watch?v=PljDuynF-j0
        # https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

        # decision order:
        # - surrender
        # - split
        # - double down
        # - hit or stand
