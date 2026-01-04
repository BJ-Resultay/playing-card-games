"""test real player"""
# Date:	27 Dec 2023
# Revision History:
#	resultay | 27-12-23 | Initial version

from pytest import MonkeyPatch
from pytest_mock import MockerFixture
import pytest
from src.general.real_player import RealPlayer

NUMBER = '777'

@pytest.fixture()
def actions() -> list[str]:
    """fixture returns list of actions"""
    return [
        'action1',
        'action2',
        'action3',
        'action44',
    ]

@pytest.fixture()
def real_player(monkeypatch: MonkeyPatch) -> RealPlayer:
    """fixture returns real player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'Jean Hugard')
    player = RealPlayer()
    monkeypatch.undo() # breakpoints use bulitin input
    return player

def test_init_real_player():
    """init real player with name"""
    name = "some name"
    player = RealPlayer(name=name)
    assert player.name == name

def test_get_choice(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get choice from player"""
    monkeypatch.setattr('builtins.input', lambda _ : actions[0])
    action = real_player.user_choice('', actions)
    assert action == actions[0]

def test_no_choices_given(real_player: RealPlayer):
    """no choices for prompt"""
    with pytest.raises(ValueError):
        real_player.user_choice('', [])

def test_get_no_choice(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get no input from player"""
    user_input = iter(['', actions[1]])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    action = real_player.user_choice('', actions)
    assert action == actions[1]

def test_get_shortened_choice(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get shortened choice from player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'action4')
    action = real_player.user_choice('', actions)
    assert action == 'action44'

def test_get_shortened_choice_error(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get shortened choice from player fails"""
    user_input = iter(['action', actions[1]])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    action = real_player.user_choice('', actions)
    assert action == actions[1]

def test_get_incorrect_choice(
    actions: list[str],
    monkeypatch: MonkeyPatch,
    real_player: RealPlayer
):
    """get incorrect choice from player"""
    user_input = iter(['abc', actions[1]])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    action = real_player.user_choice('', actions)
    assert action == actions[1]

def test_get_bet(mocker: MockerFixture, real_player: RealPlayer):
    """get bet from player"""
    mocker.patch.object(real_player, 'user_float', return_value = float(NUMBER))
    real_player.user_chips()
    assert real_player.chips == real_player.STARTING_CHIPS - float(NUMBER)

def test_get_invalid_bet(mocker: MockerFixture, real_player: RealPlayer):
    """get invalid bet from player"""
    mocker.patch.object(real_player, 'user_float', side_effect = [-420, float(NUMBER)])
    real_player.user_chips()
    assert real_player.chips == real_player.STARTING_CHIPS - float(NUMBER)

def test_get_float(monkeypatch: MonkeyPatch, real_player: RealPlayer):
    """get float from player"""
    monkeypatch.setattr('builtins.input', lambda _ : NUMBER)
    number = real_player.user_float('')
    assert number == float(NUMBER)

def test_get_invalid_float(monkeypatch: MonkeyPatch, real_player: RealPlayer):
    """get invalid float from player"""
    user_input = iter(['float', NUMBER])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    number = real_player.user_float('')
    assert number == float(NUMBER)

def test_get_integer(monkeypatch: MonkeyPatch, real_player: RealPlayer):
    """get integer from player"""
    monkeypatch.setattr('builtins.input', lambda _ : NUMBER)
    number = real_player.user_integer('')
    assert number == int(NUMBER)

def test_get_invalid_integer(monkeypatch: MonkeyPatch, real_player: RealPlayer):
    """get invalid integer from player"""
    user_input = iter(['int', NUMBER])
    monkeypatch.setattr('builtins.input', lambda _ : next(user_input))
    number = real_player.user_integer('')
    assert number == int(NUMBER)
