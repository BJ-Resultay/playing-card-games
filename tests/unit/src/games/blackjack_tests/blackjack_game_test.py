"""test blackjack"""
# Date:	13 Aug 2023
# Revision History:
#	resultay | 13-08-23 | Force load

from pytest_mock import MockerFixture
from src.games.blackjack import blackjack_game
from src.games.blackjack import blackjack_round
from src.games.blackjack.blackjack_bot import BlackjackBot
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.games.blackjack.blackjack_deck import BlackjackDeck

def test_main(
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """function plays blackjack"""
    setup = mocker.patch.object(blackjack_game, 'setup', return_value = (dealer, deck, []))
    round_ = mocker.patch.object(blackjack_game, 'play_round')
    reset = mocker.patch.object(blackjack_game, 'reset', return_value = (deck, []))

    blackjack_game.main()
    setup.assert_called_once()
    round_.assert_called()
    reset.assert_called()

def test_setup():
    """function returns dealer, deck, and players"""
    dealer, deck, players = blackjack_game.setup()
    assert isinstance(dealer, BlackjackDealer)
    assert isinstance(deck, BlackjackDeck)
    assert all(isinstance(player, BlackjackBot) for player in players)

def test_play_round(mocker: MockerFixture):
    """function plays single round"""
    start = mocker.patch.object(blackjack_round, 'start', return_value = [])
    play = mocker.patch.object(blackjack_round, 'play')
    end = mocker.patch.object(blackjack_round, 'end')

    blackjack_game.play_round('dealer', 'deck', [])
    start.assert_called_once()
    play.assert_called_once()
    end.assert_called_once()

def test_reset(deck: BlackjackDeck, mocker: MockerFixture):
    """function resets deck and players"""
    create_deck = mocker.spy(blackjack_game, 'create_deck')
    create_bots = mocker.spy(blackjack_game, 'create_bots')

    blackjack_game.reset(deck, [])
    create_deck.assert_called_once()
    create_bots.assert_called_once()

def test_no_reset(deck: BlackjackDeck, mocker: MockerFixture):
    """function does not resets deck and players"""
    create_deck = mocker.spy(blackjack_game, 'create_deck')
    create_bots = mocker.spy(blackjack_game, 'create_bots')

    blackjack_game.reset(deck * 2, [1, 2, 3, 4])
    create_deck.assert_not_called()
    create_bots.assert_not_called()
