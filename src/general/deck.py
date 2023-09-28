"""module models deck of playing cards"""
# Date:	18 Aug 2023
# Revision History:
#	resultay | 18-08-23 | Initial version

from __future__ import annotations
import random
from src.general import Face
from src.general import LOGGER
from src.general import Suit
from src.general.card import Card

class Deck():
    """class models deck of playing cards"""
    def __init__(self, extra_cards: list[Card] = None) -> None:
        """
        Args:
            extra_cards (list[Card], optional): extra cards to add to deck. Defaults to None.
        """
        self.face_down = True
        """
        intended whether cards shows face value\n
        default hidden\n
        Note: not coupled to card state themselves
        """

        self.logger = LOGGER
        """logfile handler for info"""

        self.order: list[Card] = [None] * 52
        """order of cards"""

        # A-K Hearts
        # A-K Clubs
        # K-A Diamonds
        # K-A Spades
        for i, face in enumerate(Face): # 0-12
            self.order[i] = Card(face, Suit.HEART)
        for i, face in enumerate(Face): # 13-25
            self.order[i + 13] = Card(face, Suit.CLUB)
        for i, face in enumerate(Face): # 38-26
            self.order[38 - i] = Card(face, Suit.DIAMOND)
        for i, face in enumerate(Face): # 51-39
            self.order[51 - i] = Card(face, Suit.SPADE)

        if isinstance(extra_cards, list):
            for extra_card in extra_cards:
                self.add_card(extra_card)

    def __add__(self, other: Deck) -> Deck:
        self.order += other.order
        return self

    def __mul__(self, other: int) -> Deck:
        self.order *= other
        self.logger.info('deck is %d cards large', len(self.order))
        return self

    def __rmul__(self, other: int) -> Deck:
        self.order *= other
        self.logger.info('deck is %d cards large', len(self.order))
        return self

    def add_card(self, card: Card) -> None:
        """function adds card to the bottom

        Args:
            card (Card): card added to hand
        """
        if not isinstance(card, Card):
            raise AttributeError('non cards cannot be added to the deck')
        self.order.append(card)

    def deal(self, position: int = 0) -> Card:
        """function removes card from deck

        Args:
            position (int, optional): position of card dealt. Defaults to 0.

        Raises:
            AttributeError: deck is empty
            AttributeError: position must be integer
            AttributeError: position not in range

        Returns:
            Card: card dealt
        """
        # cheaters can deal any card from the deck
        if len(self.order) == 0:
            raise AttributeError('deck is empty')
        if not isinstance(position, int):
            raise AttributeError('position must be integer')
        length = len(self.order)
        if position not in range(-length, length):
            raise AttributeError(f'position not in range {length}')
        card = self.order.pop(position)
        self.logger.debug('dealt %s', card.face_value())
        return card

    def face_values(self) -> None:
        """function returns face values of entire deck"""
        return [card.face_value() for card in self.order]

    def false_shuffle(self, indexes: list[int]) -> None:
        """function controls cards defined at index

        Args:
            indexes (list[int]): mask to order cards

        Raises:
            AttributeError: indexes must be a list
            AttributeError: indexes cannot be larger than deck
        """
        if not isinstance(indexes, list):
            raise AttributeError('indexes must be a list')
        if len(indexes) > len(self.order):
            raise AttributeError('indexes cannot be larger than deck')

        # replace
        indexes = [index if not isinstance(index, Card) else None for index in indexes]
        for i, card in enumerate(self.order):
            if i in indexes:
                indexes[indexes.index(i)] = card

        # clean
        indexes = [card if isinstance(card, Card) else None for card in indexes]
        controlled_cards = [card for card in indexes if card is not None]
        for card in controlled_cards:
            self.order.remove(card)

        # combine
        self.shuffle()
        for i, card in enumerate(indexes):
            if card is None:
                continue
            self.order.insert(i, card)

    def flip(self) -> None:
        """function flips cards and reverses order"""
        self.face_down = not self.face_down
        for card in self.order:
            card.flip()
        self.reverse()

    def remove_cards(self, to_remove: list[Card]) -> list:
        """function removes all cards from deck with both face and suit

        Args:
            to_remove (list[Card]): mask to remove cards

        Returns:
            list: removed cards
        """
        removed_cards = [card for card in self.order if card in to_remove]
        for card in removed_cards:
            self.order.remove(card)
        return removed_cards

    def remove_cards_either(
        self,
        face: Face = None,
        suit: Suit = None,
        points: int = None,
    ) -> list:
        """function removes all cards from deck with either face and suit

        Args:
            face (Face, optional): face mask. Defaults to None.
            suit (Suit, optional): suit mask. Defaults to None.
            points (int, optional): points mask. Defaults to None.

        Returns:
            list: removed cards
        """
        removed_cards = []
        for card in self.order:
            if (card.face == face
                or card.suit == suit
                or card.points == points):
                removed_cards.append(card)

        for card in removed_cards:
            self.order.remove(card)
        return removed_cards

    def reverse(self) -> None:
        """function reverses order of the deck"""
        self.order.reverse()

    def shuffle(self) -> None:
        """function shuffles order of the deck"""
        random.shuffle(self.order)
