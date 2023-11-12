"""module runs blackjack"""
#!/usr/local/bin/python3
# Date: 13 Aug 2023
# Revision History:
#   resultay | 13-08-23 | Force load

from logging import getLogger
import random
import sys
from src.games.blackjack.blackjack_bot import BlackjackBot
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack import blackjack_round

LOGGER = getLogger(__name__)

def main():
    """function runs blackjack game"""
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    LOGGER.info('Seed %d', seed)

    dealer = BlackjackDealer()
    deck = BlackjackDeck() * 2
    deck.shuffle()
    players = []
    for _ in range(1):
        players.append(BlackjackBot('Bob'))
    for _ in range(1):
        players = blackjack_round.start(dealer, deck, players)
        blackjack_round.play(dealer, deck, players)
        blackjack_round.end(dealer, players)
    return True

if __name__ == '__main__':
    main()
