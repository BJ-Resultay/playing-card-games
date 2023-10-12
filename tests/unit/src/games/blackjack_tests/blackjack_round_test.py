"""test blackjack blackjack_round"""
# Date:	08 Oct 2023
# Revision History:
#	resultay | 08-10-23 | Initial version

from pytest_mock import MockerFixture
import pytest
from src.games.blackjack import blackjack_round
from src.games.blackjack.blackjack_bot import BlackjackBot
from src.games.blackjack.blackjack_dealer import BlackjackDealer
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.constants import BlackjackError
from src.general.card import Card

ROUND = 'src.games.blackjack.blackjack_round'

@pytest.fixture()
def __compare(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
) -> None:
    """fixture mocks blackjack and bustr"""
    mocker.patch.object(bot, 'blackjack', return_value = False)
    mocker.patch.object(bot.hand, 'bust', return_value = False)
    mocker.patch.object(dealer, 'blackjack', return_value = False)
    mocker.patch.object(dealer.hand, 'bust', return_value = False)

def test_start(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """bots bet and cards are dealt"""
    bet = mocker.patch(f'{ROUND}.bet', return_value = [])
    deal = mocker.patch(f'{ROUND}.deal')

    players = blackjack_round.start(dealer, deck, [bot])
    assert players == []
    bet.assert_called_once_with([bot])
    deal.assert_called_once_with(dealer, deck, [])

def test_bet(bot: BlackjackBot):
    """bot bets minimum chips"""
    bot.chips = blackjack_round.MINIMUM_BET
    players = blackjack_round.bet([bot])
    assert players == [bot]
    assert bot.bet == blackjack_round.MINIMUM_BET
    assert bot.chips == 0

def test_no_bet(bot: BlackjackBot):
    """bot cannot bet"""
    bot.chips = 0
    players = blackjack_round.bet([bot])
    assert players == []

def test_deal(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
):
    """
    players get two face up cards
    and dealers get one face up and one face down
    """
    blackjack_round.deal(dealer, deck * 2, [bot])
    assert len(dealer.hand) == 2
    assert len(bot.hand) == 2
    assert not dealer.hand[0].face_down
    assert dealer.hand[1].face_down
    assert not bot.hand[0].face_down
    assert not bot.hand[1].face_down

def test_deal_error(deck: BlackjackDeck):
    """deck too small"""
    with pytest.raises(BlackjackError):
        blackjack_round.deal(None, deck, [])

def test_play(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """bot and dealer takes turn"""
    bot_turn = mocker.patch.object(bot, 'turn')
    dealer_turn = mocker.patch.object(dealer, 'turn')

    blackjack_round.play(dealer, deck, [bot])
    bot_turn.assert_called_once_with(0, deck)
    dealer_turn.assert_called_once_with(deck)

def test_end(
    ace: Card,
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """
    players wins and discard
    dealer discards
    """
    mocker.patch(f'{ROUND}.compare', return_value = [2])
    bot.add_card(ace)
    bot.bet_chips(5)
    dealer.add_card(ace)
    blackjack_round.end(dealer, [bot])
    assert len(bot.hand) == 0
    assert bot.chips == bot.STARTING_CHIPS + 5
    assert bot.bet == 0
    assert len(dealer.hand) == 0

def test_compare_blackjacks(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """tie if player and dealer get blackjack"""
    mocker.patch.object(bot, 'blackjack', return_value = True)
    mocker.patch.object(dealer, 'blackjack', return_value = True)
    tie = blackjack_round.compare(dealer, bot)
    assert tie == [1]

def test_compare_dealer_blackjack(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """lose if dealer gets blackjack"""
    mocker.patch.object(dealer, 'blackjack', return_value = True)
    lose = blackjack_round.compare(dealer, bot)
    assert lose == [0]

def test_compare_player_blackjack(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """win if player gets blackjack"""
    mocker.patch.object(bot, 'blackjack', return_value = True)
    win = blackjack_round.compare(dealer, bot)
    assert win == [2.5]

def test_compare_player_bust(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """lose if player bust"""
    # still lose if dealer also bust
    mocker.patch.object(bot.hand, 'bust', return_value = True)
    lose = blackjack_round.compare(dealer, bot)
    assert lose == [0]

def test_compare_dealer_bust(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """win if dealer bust and player did not"""
    mocker.patch.object(dealer.hand, 'bust', return_value = True)
    win = blackjack_round.compare(dealer, bot)
    assert win == [2]

def test_compare_player_score_win(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """win if player score is greater"""
    mocker.patch.object(bot.hand, 'score', return_value = 21)
    mocker.patch.object(dealer.hand, 'score', return_value = 20)
    win = blackjack_round.compare(dealer, bot)
    assert win == [2]

def test_compare_player_score_lose(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """lose if player score is smaller"""
    mocker.patch.object(bot.hand, 'score', return_value = 20)
    mocker.patch.object(dealer.hand, 'score', return_value = 21)
    lose = blackjack_round.compare(dealer, bot)
    assert lose == [0]

def test_compare_player_score_tie(
    bot: BlackjackBot,
    dealer: BlackjackDealer,
    mocker: MockerFixture,
):
    """tie if player score is equal"""
    mocker.patch.object(bot.hand, 'score', return_value = 21)
    mocker.patch.object(dealer.hand, 'score', return_value = 21)
    lose = blackjack_round.compare(dealer, bot)
    assert lose == [1]
