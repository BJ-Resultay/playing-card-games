"""module models actual blackjack player"""
# Date:	03 Feb 2024
# Revision History:
#	resultay | 03-02-24 | Initial version

import itertools
from logging import getLogger
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.blackjack_player import BlackjackPlayer
from src.games.blackjack.constants import BlackjackError
from src.general.real_player import RealPlayer

LOGGER = getLogger(__name__)

class BlackjackRealPlayer(BlackjackPlayer, RealPlayer):
    """class models actual blackjack player"""
    def __init__(self) -> None:
        super().__init__()
        self.logger = LOGGER

    def turn(self, dealer_score: int, deck: BlackjackDeck):
        """function decides player's decisions for their turn

        Args:
            dealer_score (int): used in player prompt
            deck (BlackjackDeck): deck player draws from
        """
        hands = iter(self.hands)
        self.hand = next(hands)
        self.logger.info("%s's turn starts", self.name)
        while not self.hands[-1].end:
            move = self.user_move(dealer_score)
            match move:
                case "surrender":
                    self.surrender()
                case "split":
                    card1 = deck.draw()
                    card2 = deck.draw()
                    self.split(card1, card2)
                case "double down":
                    card = deck.draw()
                    self.double_down(card)
                case "stand":
                    self.stand()
                case "hit":
                    card = deck.draw()
                    self.hit(card)
            if self.hand.end:
                self.hand = next(hands)

    def user_move(self, dealer_score: int):
        """function interprets input as valid move

        Args:
            dealer_score (int): used in player prompt

        Raises:
            BlackjackError: player has no valid moves

        Returns:
            str: input as valid move
        """
        all_moves = [
            "surrender",
            "split",
            "double down"
            "stand",
            "hit"
        ]
        valid_moves_mask = [
            self.can_surrender(),
            self.can_split(),
            self.can_double_down(),
            self.can_stand(),
            self.can_hit()
        ]
        valid_moves = list(itertools.compress(all_moves, valid_moves_mask))
        if not valid_moves:
            self.cards()
            raise BlackjackError(f'{self.name} has no valid moves')
        return self.user_choice(f"{dealer_score}\nChoose move:", valid_moves)
