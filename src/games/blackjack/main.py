"""module runs blackjack"""
# Date: 13 Aug 2023
# Revision History:
#   resultay | 13-08-23 | Force load

from logging import getLogger
from names import get_first_name
from src.games.blackjack import blackjack_round
from src.games.blackjack.blackjack_bot import BlackjackBot
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.general.games import set_seed

LOGGER = getLogger(__name__)
"""logfile handler for info"""

NUM_DECKS = 6
"""number of decks combined"""

NUM_BOTS = 4
"""number of other players"""

def main():
    """function runs blackjack game"""
    dealer, deck, players = setup()

    for _ in range(10):
        play_round(dealer, deck, players)
        deck, players = reset(deck, players)
    return True

def setup() -> tuple[BlackjackDealer, BlackjackDeck, list[BlackjackBot]]:
    """function sets up blackjack game

    Returns:
        tuple[
            BlackjackDealer,
            BlackjackDeck,
            list[BlackjackBot]
        ]: initial dealer, deck, and players
    """
    # Debug: pass seed as parameter
    seed = set_seed()
    LOGGER.info('Set seed %d', seed)

    dealer = BlackjackDealer()
    deck = create_deck()
    players = create_bots()

    return dealer, deck, players

def create_deck() -> BlackjackDeck:
    """function returns shuffled deck

    Returns:
        BlackjackDeck: shuffled deck
    """
    deck = BlackjackDeck() * NUM_DECKS
    deck.shuffle()
    return deck

def create_bots() -> list[BlackjackBot]:
    """function returns bots

    Returns:
        list[BlackjackBot]: other CPUs
    """
    return [BlackjackBot(get_first_name()) for _ in range(NUM_BOTS)]

def play_round(
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    players: list[BlackjackBot],
) -> None:
    """function plays round

    Args:
        dealer (BlackjackDealer): opponent
        deck (BlackjackDeck): deals cards
        players (list[BlackjackBot]): plays against dealer
    """
    players = blackjack_round.start(dealer, deck, players)
    blackjack_round.play(dealer, deck, players)
    blackjack_round.end(dealer, players)

def reset(
    deck: BlackjackDeck,
    players: BlackjackBot
) -> tuple[BlackjackDeck, list[BlackjackBot]]:
    """reset deck and players

    Args:
        deck (BlackjackDeck): old deck
        players (BlackjackBot): old players

    Returns:
        tuple[
            BlackjackDeck,
            list[BlackjackBot]
        ]: new deck and players
    """
    if len(deck.order) < blackjack_round.MINIMUM_DECK_LENGTH:
        deck = create_deck()
    if len(players) < NUM_BOTS:
        players = create_bots()
    return deck, players
