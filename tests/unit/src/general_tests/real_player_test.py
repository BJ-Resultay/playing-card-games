"""test real player"""
# Date:	27 Dec 2023
# Revision History:
#	resultay | 27-12-23 | Initial version

from pytest import MonkeyPatch
import pytest
from src.general.real_player import RealPlayer

@pytest.fixture()
def actions() -> list[str]:
    """fixture returns list of actions"""
    return [
        'action1',
        'action2',
        'action3'
    ]

@pytest.fixture()
def real_player(monkeypatch: MonkeyPatch) -> RealPlayer:
    """fixture returns real player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'Jean Hugard')
    player = RealPlayer()
    monkeypatch.undo() # breakpoints use bulitin input
    return player

def test_get_input(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get input from player"""
    monkeypatch.setattr('builtins.input', lambda _ : actions[0])
    action = real_player.multiple_choice('', actions)
    assert action == actions[0]

def test_get_no_input(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get no from player"""
    user_input = iter(['', actions[1]])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    action = real_player.multiple_choice('', actions)
    assert action == actions[1]

def test_get_shortened_input(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get shortened input from player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'action')
    action = real_player.multiple_choice('', actions)
    assert action == actions[0]

def test_get_shorthand_input(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get shorthand input from player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'a2')
    action = real_player.multiple_choice('', actions)
    assert action == actions[1]
