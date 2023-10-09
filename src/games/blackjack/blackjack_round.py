"""module models blackjack round"""
# Date:	01 Oct 2023
# Revision History:
#	resultay | 01-10-23 | Initial version

from logging import getLogger
from src.games.blackjack.blackjack_bot import BlackjackBot
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.constants import BlackjackError

LOGGER = getLogger(__name__)
"""logfile handler for info"""

MINIMUM_BET = 2
"""chips required to play"""

MINIMUM_DECK_LENGTH = 60
"""unused cards to counteract card counting"""

def start(
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    players: list[BlackjackBot],
) -> None:
    """function sets up round

    Args:
        dealer (BlackjackDealer): gets one face up card and once face down card
        deck (BlackjackDeck): draw cards
        players (list[BlackjackBot]): bets and gets two face up cards
    """
    LOGGER.info('Round starting')
    players = bet(players)
    deal(dealer, deck, players)

def bet(players: list[BlackjackBot]) -> list[BlackjackBot]:
    """function filters players that can pay the minimum bet

    Args:
        players (list[BlackjackBot]): full set of players

    Returns:
        list[BlackjackBot]: subset of players that can bet
    """
    betting_players = [player for player in players if player.chips >= MINIMUM_BET]
    for player in players:
        if player in betting_players:
            player.bet_chips(MINIMUM_BET)
        else:
            LOGGER.info('%s cannot pay minimum bet', player.name)
    return betting_players

def deal(
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    players: list[BlackjackBot],
) -> None:
    """function deals cards to players

    Args:
        dealer (BlackjackDealer): gets one face up card and once face down card
        deck (BlackjackDeck): draw cards
        players (list[BlackjackBot]): gets two face up cards

    Raises:
        BlackjackError: deck is smaller than minimum length
    """
    deck_length = len(deck.order)
    if deck_length < MINIMUM_DECK_LENGTH:
        raise BlackjackError(f'deck length {deck_length} is smaller than {MINIMUM_DECK_LENGTH}')
    LOGGER.info('Dealing cards to players')
    for i in range(2):
        for player in (players + [dealer]):
            card = deck.draw()
            if (player == dealer
                and i == 1):
                card.flip()
            player.add_card(card)

    for player in players:
        LOGGER.info(
            "%s hand: %02d, %s",
            player.name,
            player.hand.score(),
            ' '.join(player.hand.face_values())
        )
    LOGGER.info(
        "%s hand: %02d, %s **",
        dealer.name,
        dealer.hand.score(),
        dealer.hand[0].face_value()
    )

def end(dealer: BlackjackDealer, players: list[BlackjackBot]) -> None:
    """function compares scores, collect and payout bets, and discards hands

    Args:
        dealer (BlackjackDealer): compare score and discard
        players (list[BlackjackBot]): compare score, win or lose chips, discard
    """
    LOGGER.info('Round ending')
    for player in ([dealer] + players):
        LOGGER.info('%s hand:', player.name)
        for hand in player.hands:
            LOGGER.info('%02d, %s', hand.score(), ' '.join(hand.face_values()))
    for player in players:
        winnings = compare(dealer, player)
        for winning in winnings:
            player.bet_win(winning)
        player.bet = 0
        player.discard_cards()
    dealer.discard_cards()

def compare(dealer: BlackjackDealer, player: BlackjackBot) -> list[int | float]:
    """function compares scores

    Args:
        dealer (BlackjackDealer): check score, bust, blackjack
        player (BlackjackBot): lose, tie, or win

    Returns:
        list[int | float]: modifiers [0, 1, 2, 2.5]
    """
    if dealer.blackjack():
        if player.blackjack():
            return [1]
        return [0]
    if player.blackjack():
        return [2.5]
    winnings = []
    dealer_score = dealer.hand.score()
    for hand in player.hands:
        player_score = hand.score()
        # players lose on bust even if dealer busts
        if hand.bust():
            winnings.append(0)
        elif (dealer.hand.bust()
              or player_score > dealer_score):
            winnings.append(2)
        elif player_score < dealer_score:
            winnings.append(0)
        else:
            winnings.append(1)
    return winnings
