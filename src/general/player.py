"""module models general player"""
# Date:	20 Aug 2023
# Revision History:
#	resultay | 20-08-23 | Initial version

from logging import getLogger
import math
from src.general import Face
from src.general import Suit
from src.general.card import Card

LOGGER = getLogger(__name__)

class Player():
    """class models general player"""
    STARTING_CHIPS = 3000.00

    def __init__(self, name: str):
        """
        Args:
            name (str): distinguish players in human readable format
        """
        self.bet = 0
        """bet for winning and losing chips"""

        self.chips = self.STARTING_CHIPS
        """amount player can still bet"""

        self.hand: list[Card] = []
        """cards player can use"""

        self.logger = LOGGER
        """logfile handler for info"""

        self.name = name
        """name to differentiate between other players"""

        self.stats = {}
        """statistics keep track of milestones"""

    def add_card(self, card: Card) -> None:
        """function adds card to hand and sorts

        Args:
            card (Card): card added to hand

        Raises:
            AttributeError: only add cards to hand
        """
        # NOTE: covered in other tests
        if self.logger == LOGGER:
            self.logger.info('%s added card', self.name)
        if not isinstance(card, Card):
            raise AttributeError('only add cards to hand')
        self.hand.append(card)
        self.sort_hand()

    def bet_chips(self, chips: float) -> None:
        """function moves chips to bet

        Args:
            chips (float): chips used to bet

        Raises:
            AttributeError: chips must be positive number
            AttributeError: chips must be positive
            AttributeError: not enough chips to bet
        """
        if not isinstance(chips, (float, int)):
            raise AttributeError('chips must be positive number')
        chips = round(float(chips), 2)
        self.logger.info('%s bet $%d', self.name, chips)
        if chips <= 0:
            raise AttributeError('chips must be positive')
        if self.chips < chips:
            raise AttributeError('not enough chips to bet')
        self.bet += chips
        self.chips -= chips

    def bet_win(self, multiplier: float = 2.0) -> None:
        """function moves bet to chips

        Args:
            multiplier (float, optional): determines winning amount. Defaults to 2.0.

        Raises:
            AttributeError: multiplier must be positive number
            AttributeError: multiplier must be positive
        """
        # default 1:1
        if not isinstance(multiplier, (float, int)):
            raise AttributeError('multiplier must be positive number')
        multiplier = float(multiplier)
        if multiplier < 0:
            raise AttributeError('multiplier must be positive')
        winnings = round(self.bet * multiplier, 2)
        self.logger.info('%s won $%d', self.name, winnings)
        self.chips += winnings

    def increase_stat(self, stat: str) -> None:
        """function increases statistic

        Args:
            stat (str): stat to be raised

        Raises:
            AttributeError: stat must be string
        """
        if not isinstance(stat, str):
            raise AttributeError('stat must be string')
        try:
            self.stats[stat] += 1
        except KeyError:
            self.stats[stat] = 1

    def sort_hand(self) -> None:
        """function sorts cards in hand"""
        faces = list(Face) # A-K
        suits = list(Suit) # CDHS
        def face_value_to_int(card: Card) -> int:
            """sorts cards by suit then face

            Args:
                card (Card): card to sort

            Returns:
                int: card position
            """
            try:
                face = faces.index(card.face) # 0-12
                suit = suits.index(card.suit) # 0-3
                return suit * 13 + face
            except ValueError:
                return math.inf

        self.hand.sort(key = face_value_to_int)
