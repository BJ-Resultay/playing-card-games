"""module models general player"""
# Date:	20 Aug 2023
# Revision History:
#	resultay | 20-08-23 | Initial version

import math
from src.constants import Face
from src.constants import Suit
from src.general.card import Card

class Player():
    """class models general player"""
    STARTING_CHIPS = 3000.00

    def __init__(self, name: str):
        self.bet = 0
        self.chips = self.STARTING_CHIPS
        self.hand: list[Card] = []
        self.name = name
        self.stats = {}

    def add_card(self, card: Card) -> None:
        """function adds card to hand and sorts"""
        if not isinstance(card, Card):
            raise AttributeError('only add cards to hand')
        self.hand.append(card)

    def bet_chips(self, chips: float) -> None:
        """function moves chips to bet"""
        if not isinstance(chips, (float, int)):
            raise AttributeError('chips must be positive number')
        chips = round(float(chips), 2)
        if chips <= 0:
            raise AttributeError('chips must be positive')
        if self.chips < chips:
            raise AttributeError('not enough chips to bet')
        self.bet += chips
        self.chips -= chips

    def bet_win(self, multiplier: float = 2.0) -> None:
        """function moves bet to chips"""
        # default 1:1
        if not isinstance(multiplier, (float, int)):
            raise AttributeError('multiplier must be positive number')
        multiplier = float(multiplier)
        if multiplier < 1:
            raise AttributeError('multiplier must be at least 1.0')
        self.chips += round(self.bet * multiplier, 2)
        self.bet = 0

    def increase_stat(self, stat: str) -> None:
        """function increases statistic"""
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
            """sorts cards by suit then face"""
            try:
                face = faces.index(card.face) # 0-12
                suit = suits.index(card.suit) # 0-3
                return suit * 13 + face
            except ValueError:
                return math.inf

        self.hand.sort(key = face_value_to_int)
