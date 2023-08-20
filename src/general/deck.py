"""module models deck of playing cards"""
# Date:	18 Aug 2023
# Revision History:
#	resultay | 18-08-23 | Initial version

import random
from src.constants import Face
from src.constants import Suit
from src.general import Card

class Deck():
    """class models deck of playing cards"""
    def __init__(self, extra_cards: list[Card] = None) -> None:
        self.order = [None] * 52
        self.face_down = True

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

    def add_card(self, card: Card) -> None:
        """function adds card to the bottom"""
        if not isinstance(card, Card):
            raise AttributeError('non cards cannot be added to the deck')
        self.order.append(card)

    def deal(self, position: int = 0) -> Card:
        """function removes card from deck"""
        # cheaters can deal any card from the deck
        if not isinstance(position, int):
            raise AttributeError('position must be integer')
        length = len(self.order)
        if position not in range(-length, length):
            raise AttributeError(f'position not in range {length}')
        return self.order.pop(position)

    def face_values(self) -> None:
        """function returns face values of entire deck"""
        return [card.face_value() for card in self.order]

    def false_shuffle(self, indexes: list[int]) -> None:
        """function controls cards defined at index"""
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
        """
        function removes all cards from deck with both face and suit
        returns removed cards
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
        """
        function removes all cards from deck with either face and suit
        returns removed cards
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
