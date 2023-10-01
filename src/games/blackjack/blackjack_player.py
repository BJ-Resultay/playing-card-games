"""module models blackjack player"""
# Date:	26 Aug 2023
# Revision History:
#	resultay | 26-08-23 | Initial version

from logging import getLogger
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.blackjack_hand import BlackjackHand
from src.games.blackjack.constants import BLACKJACK, BlackjackError
from src.general.card import Card
from src.general.player import Player

LOGGER = getLogger(__name__)

class BlackjackPlayer(Player):
    """class models blackjack player"""
    def __init__(self, name: str):
        """
        Args:
            name (str): distinguish players in human readable format
        """
        super().__init__(name)
        self.hands: list[BlackjackHand] = [BlackjackHand()]
        """split allows multiple hands"""

        self.hand: BlackjackHand = self.hands[0]
        """cards player has"""

        self.logger = LOGGER
        """logfile handler for info"""

        self.stats[BLACKJACK] = {}

    def blackjack(self) -> bool:
        """function checks for blackjack

        Returns:
            bool: if player has blackjack
        """
        return (self.hand.score() == 21
                and len(self.hand) == 2
                and len(self.hands) == 1)

    def can_double_down(self) -> bool:
        """function checks if player can double down

        Returns:
            bool: if player can double down
        """
        return (len(self.hand) == 2
                and self.chips >= self.bet)

    def can_hit(self) -> bool:
        """function checks if player can hit

        Returns:
            bool: if player can hit
        """
        return not self.hand.bust()

    def can_split(self) -> bool:
        """function checks if player can split

        Returns:
            bool: if player can split
        """
        return (len(self.hand) == 2
                and self.hand[0].face == self.hand[1].face
                and self.chips >= self.bet)

    def can_stand(self) -> bool:
        """function checks if player can stand

        Returns:
            bool: if player can stand
        """
        return len(self.hand) >= 2

    def can_surrender(self) -> bool:
        """function checks if player can surrender

        Returns:
            bool: if player can surrender
        """
        return len(self.hands) == 1 and len(self.hand) == 2

    def discard_cards(self) -> None:
        """function empties hand"""
        self.hands = [BlackjackHand()]
        self.hand = self.hands[0]

    def double_down(self, card: Card) -> None:
        """function bets and only take one hand

        Args:
            card (Card): card hit

        Raises:
            BlackjackError: cannot double down with hand
        """
        self.logger.info('%s doubled down', self.name)
        if not self.can_double_down():
            raise BlackjackError(f'cannot double down with hand {self.hand.face_values()}')

        self.add_card(card)
        self.hand.double = True
        self.hand.end = True
        self.chips -= self.bet

        if self.hand.bust():
            self.logger.info('%s busted', self.name)

    def draw(self, deck: BlackjackDeck) -> Card:
        """function draws card from deck

        Args:
            deck (BlackjackDeck): deck player draws cards from

        Returns:
            Card: card player drew
        """
        if not deck.face_down:
            self.logger.warning('deck was not face down')
            deck.flip()
        card = deck.deal()
        card.flip()
        return card

    def hit(self, card: Card) -> None:
        """function adds card to hand

        Args:
            card (Card): card hit

        Raises:
            BlackjackError: cannot hit with hand
        """
        self.logger.info('%s hit', self.name)
        if not self.can_hit():
            raise BlackjackError(f'cannot hit with hand {self.hand.face_values()}')

        self.add_card(card)
        if self.hand.bust():
            self.logger.info('%s busted', self.name)
            self.hand.end = True

    def increase_stat(self, stat: str) -> None:
        """override: increases blackjack statistic

        Args:
            stat (str): stat to inc

        Raises:
            AttributeError: stat must be string
        """
        if not isinstance(stat, str):
            raise AttributeError('stat must be string')
        try:
            self.stats[BLACKJACK][stat] += 1
        except KeyError:
            self.stats[BLACKJACK][stat] = 1

    def split(self, card1: Card, card2: Card):
        """function bets and cuts hand in half

        Args:
            card1 (Card): card hit current hand
            card2 (Card): card hit other hand

        Raises:
            BlackjackError: cannot split with hand
        """
        self.logger.info('%s split', self.name)
        if not self.can_split():
            raise BlackjackError(f'cannot split with hand {self.hand.face_values()}')

        other_hand = self.hand.split()
        self.hands.append(other_hand)
        self.add_card(card1)

        current_hand = self.hands.index(self.hand)
        self.hand = self.hands[-1]
        self.add_card(card2)
        self.hand = self.hands[current_hand]

        self.chips -= self.bet

    def stand(self) -> None:
        """function ends hand

        Raises:
            BlackjackError: cannot stand with hand
        """
        self.logger.info('%s stood', self.name)
        if not self.can_stand():
            raise BlackjackError(f'cannot stand with hand {self.hand.face_values()}')

        self.hand.end = True

    def surrender(self) -> None:
        """function cuts bet in half

        Raises:
            BlackjackError: cannot surrender with hand
        """
        self.logger.info('%s surrendered', self.name)
        if not self.can_surrender():
            raise BlackjackError(f'cannot surrender with hand {self.hand.face_values()}')

        self.bet_win(0.5)
        self.hand.end = True
