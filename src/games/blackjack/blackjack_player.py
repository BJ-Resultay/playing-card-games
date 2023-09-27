"""module models blackjack player"""
# Date:	26 Aug 2023
# Revision History:
#	resultay | 26-08-23 | Initial version

# https://www.youtube.com/watch?v=PljDuynF-j0
# https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

# decision order:
# - surrender
# - split
# - double down
# - hit or stand

from src.games.blackjack import LOGGER
from src.games.blackjack.blackjack_hand import BlackjackHand
from src.games.blackjack.constants import BLACKJACK
from src.games.blackjack.constants import BlackjackError
from src.general import Face
from src.general.card import Card
from src.general.player import Player

class BlackjackPlayer(Player):
    """class models blackjack player"""
    def __init__(self, name: str):
        super().__init__(name)
        self.hands: list[BlackjackHand] = [BlackjackHand()]
        """split allows multiple hands"""

        self.hand: BlackjackHand = self.hands[0]
        """cards player has"""

        self.logger = LOGGER
        """
        logfile handler for info\n
        default logs/blackjack.log
        """

        self.stats[BLACKJACK] = {}

    def blackjack(self) -> bool:
        """function checks for blackjack"""
        return (self.hand.score() == 21
                and len(self.hand) == 2
                and len(self.hands) == 1)

    def can_double_down(self) -> bool:
        """function checks if player can double down"""
        return (len(self.hand) == 2
                and self.chips >= self.bet)

    def can_hit(self) -> bool:
        """function checks if player can hit"""
        return not self.hand.bust()

    def can_split(self) -> bool:
        """function checks if player can split"""
        return (len(self.hand) == 2
                and self.hand[0].face == self.hand[1].face
                and self.chips >= self.bet)

    def can_stand(self) -> bool:
        """function checks if player can stand"""
        return len(self.hand) >= 2

    def can_surrender(self) -> bool:
        """function checks if player can surrender"""
        return len(self.hands) == 1 and len(self.hand) == 2

    def discard_cards(self) -> None:
        """function empties hand"""
        self.hands = [BlackjackHand()]
        self.hand = self.hands[0]

    def double_down(self, card: Card) -> None:
        """function bets and only take one hand"""
        self.logger.info('%s doubled down', self.name)
        if not self.can_double_down():
            raise BlackjackError(f'cannot double down with hand {self.hand.face_values()}')

        self.add_card(card)
        self.hand.double = True
        self.hand.end = True
        self.chips -= self.bet

        if self.hand.bust():
            self.logger.info('%s busted', self.name)

    def hit(self, card: Card) -> None:
        """function adds card to hand"""
        self.logger.info('%s hit', self.name)
        if not self.can_hit():
            raise BlackjackError(f'cannot hit with hand {self.hand.face_values()}')

        self.add_card(card)
        if self.hand.bust():
            self.logger.info('%s busted', self.name)
            self.hand.end = True

    def increase_stat(self, stat: str) -> None:
        """override: increases blackjack statistic"""
        if not isinstance(stat, str):
            raise AttributeError('stat must be string')
        try:
            self.stats[BLACKJACK][stat] += 1
        except KeyError:
            self.stats[BLACKJACK][stat] = 1

    def should_double_down(self, dealer_score: int) -> bool:
        """function checks whether to double down"""
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
        """function checks whether to split"""
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
        """function checks whether to stand"""
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
        """function checks whether to surrender"""
        # 16 surrenders against dealer 9 through Ace
        # 15 surrenders against dealer 10
        score = self.hand.score()
        if score == 16 and dealer_score in [9, 10, 11]:
            return True
        if score == 15 and dealer_score == 10:
            return True
        return False

    def split(self, card1: Card, card2: Card):
        """function bets and cuts hand in half"""
        self.logger.info('%s split', self.name)
        if not self.can_surrender():
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
        """function ends hand"""
        self.logger.info('%s stood', self.name)
        if not self.can_stand():
            raise BlackjackError(f'cannot stand with hand {self.hand.face_values()}')

        self.hand.end = True

    def surrender(self) -> None:
        """function cuts bet in half"""
        self.logger.info('%s surrendered', self.name)
        if not self.can_surrender():
            raise BlackjackError(f'cannot surrender with hand {self.hand.face_values()}')

        self.bet_win(0.5)
        self.hand.end = True
