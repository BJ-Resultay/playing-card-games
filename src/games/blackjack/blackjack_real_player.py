"""module models actual blackjack player"""
# Date:	03 Feb 2024
# Revision History:
#	resultay | 03-02-24 | Initial version

from logging import getLogger
from src.games.blackjack.blackjack_player import BlackjackPlayer
from src.general.real_player import RealPlayer

LOGGER = getLogger(__name__)

class BlackjackRealPlayer(BlackjackPlayer, RealPlayer):
    """class models actual blackjack player"""
    def __init__(self) -> None:
        name = input('Enter name: ')
        super().__init__(name)
        self.logger = LOGGER
