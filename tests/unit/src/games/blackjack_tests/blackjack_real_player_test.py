"""test blackjack real player"""
# Date:	28 Dec 2023
# Revision History:
#	resultay | 28-12-25 | Initial version

from pytest import MonkeyPatch
import pytest
from src.games.blackjack.blackjack_real_player import BlackjackRealPlayer

@pytest.fixture()
def player(monkeypatch: MonkeyPatch) -> BlackjackRealPlayer:
    """fixture returns blackjack real player"""
    monkeypatch.setattr('builtins.input', lambda _ : 'Bill Beater')
    player = BlackjackRealPlayer()
    monkeypatch.undo() # breakpoints use bulitin input
    return player

def test_hi(player: BlackjackRealPlayer):
    """hi"""
    pass
