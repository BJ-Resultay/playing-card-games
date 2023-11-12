"""module models blackjack dealer"""
# Date:	21 Sep 2023
# Revision History:
#	resultay | 21-09-23 | Initial version

from logging import getLogger
import math
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.blackjack_player import BlackjackPlayer
from src.games.blackjack.constants import BlackjackError
from src.general import Face
from src.general import Suit
from src.general.card import Card

LOGGER = getLogger(__name__)

class BlackjackDealer(BlackjackPlayer):
    """class models blackjack dealer"""
    def __init__(self):
        super().__init__('Dealer')
        self.logger = LOGGER

    def can_double_down(self) -> bool:
        """override: dealer cannot double down

        Returns:
            bool: False
        """
        return False

    def can_hit(self) -> bool:
        """extension: dealer cannot hit if a card is face down

        Returns:
            bool: if dealer can hit
        """
        return (super().can_hit()
                and all(not card.face_down for card in self.hand))

    def can_split(self) -> bool:
        """override: dealer cannot split

        Returns:
            bool: False
        """
        return False

    def can_stand(self) -> bool:
        """extension: dealer can stand on 17+

        Returns:
            bool: if dealer can stand
        """
        # dealer hits on soft 17
        score = self.hand.score()
        return (super().can_stand()
                and score >= 17
                and not (self.hand.soft() and score == 17))

    def can_surrender(self) -> bool:
        """override: dealer cannot surrender

        Returns:
            bool: False
        """
        return False

    def flip(self) -> None:
        """flips face down card"""
        # position dependent on sort
        card = self.hand[-1]
        card.flip()

    def sort_hand(self) -> None:
        """override: dealer leaves face down card last"""
        faces = list(Face) # A-K
        suits = list(Suit) # CDHS
        def face_value_to_int(card: Card) -> int:
            """sorts cards by face down then suit and face

            Args:
                card (Card): card to sort

            Returns:
                int: card position
            """
            if card.face_down:
                return math.inf
            face = faces.index(card.face) # 0-12
            suit = suits.index(card.suit) # 0-3
            return suit * 13 + face

        self.hand.sort(key = face_value_to_int)

    def turn(self, deck: BlackjackDeck):
        """function decides dealer's decisions for their turn

        Args:
            deck (BlackjackDeck): deck dealer draws from

        Raises:
            BlackjackError: dealer cannot hit or stand
        """
        self.logger.info("Dealer's turn starts")
        self.hand[-1].flip()
        while not self.hand.end:
            if self.can_stand():
                self.stand()
            elif self.can_hit():
                card = deck.draw()
                self.hit(card)
            else:
                self.cards()
                raise BlackjackError('dealer cannot hit or stand')
