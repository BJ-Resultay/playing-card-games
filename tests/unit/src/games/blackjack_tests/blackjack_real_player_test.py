"""test blackjack real player"""
# Date:	28 Dec 2023
# Revision History:
#	resultay | 28-12-25 | Initial version

from pytest import MonkeyPatch
from pytest_mock import MockerFixture
import pytest
from src.games.blackjack.blackjack_real_player import BlackjackRealPlayer
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.constants import BlackjackError
from src.general.card import Card

@pytest.fixture()
def player(monkeypatch: MonkeyPatch) -> BlackjackRealPlayer:
    """fixture returns blackjack real player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'Bill Beater')
    player = BlackjackRealPlayer()
    monkeypatch.undo() # breakpoints use bulitin input
    return player

def test_turn(
    ace: Card,
    player: BlackjackRealPlayer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
    monkeypatch: MonkeyPatch,
):
    """player splits, doubles down, and hits, then stand"""
    user_input = iter([
        'split',
        'double down',
        'hit',
        'stand'
    ])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    split = mocker.spy(player, 'split')
    double_down = mocker.spy(player, 'double_down')
    hit = mocker.spy(player, 'hit')
    stand = mocker.spy(player, 'stand')

    player.hand.append(ace)
    player.hand.append(ace)
    player.turn(0, deck)
    split.assert_called_once()
    double_down.assert_called_once()
    hit.assert_called_once()
    stand.assert_called_once()

def test_turn_surrender(
    player: BlackjackRealPlayer,
    deck: BlackjackDeck,
    mocker: MockerFixture,
    monkeypatch: MonkeyPatch,
):
    """player surrenders"""
    mocker.patch.object(player, 'can_surrender', return_value = True)
    monkeypatch.setattr('builtins.input', lambda _ : "surrender")
    surrender = mocker.spy(player, 'surrender')

    player.turn(0, deck)
    surrender.assert_called_once()

def test_no_valid_user_move(
    player: BlackjackRealPlayer,
    mocker: MockerFixture
):
    """player has no valid moves"""
    mocker.patch.object(player, 'can_surrender', return_value = False)
    mocker.patch.object(player, 'can_split', return_value = False)
    mocker.patch.object(player, 'can_double_down', return_value = False)
    mocker.patch.object(player, 'can_stand', return_value = False)
    mocker.patch.object(player, 'can_hit', return_value = False)

    with pytest.raises(BlackjackError):
        player.user_move(0)
