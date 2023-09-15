"""test blackjack hand"""
# Date:	14 Sep 2023
# Revision History:
#	resultay | 14-09-23 | Initial version

import pytest
from src.games.blackjack.blackjack_hand import BlackjackHand
from src.general.card import Card

@pytest.fixture()
def hand() -> BlackjackHand:
    """fixture returns blackjack hand"""
    return BlackjackHand()

def test_bust_true(hand: BlackjackHand, non_ace: Card):
    """hand busts"""
    for _ in range(3):
        hand.append(non_ace)
    assert hand.bust()

def test_bust_false(hand: BlackjackHand, non_ace: Card):
    """hand does not busts"""
    for _ in range(2):
        hand.append(non_ace)
    assert not hand.bust()

def test_face_values(ace: Card, hand: BlackjackHand):
    """returns face values"""
    hand.append(ace)
    assert ace.face_value() in hand.face_values()

def test_score(
    ace: Card,
    hand: BlackjackHand,
    non_ace: Card,
):
    """score adds up correctly"""
    hand.append(ace)
    hand.append(non_ace)
    assert hand.score() == 21

def test_score_ignore_face_down(
    ace: Card,
    hand: BlackjackHand,
    non_ace: Card,
):
    """score ignores face down cards"""
    hand.append(ace)
    hand.append(non_ace)
    non_ace.flip()
    assert hand.score() == 11

def test_score_aces_are_one(ace: Card, hand: BlackjackHand):
    """aces become one if 11 would bust"""
    hand.append(ace)
    hand.append(ace)
    assert hand.score() == 12

def test_score_ace_bust(
    ace: Card,
    hand: BlackjackHand,
    non_ace: Card,
):
    """aces become one if 1 would bust"""
    hand.append(ace)
    hand.append(non_ace)
    hand.append(non_ace)
    hand.append(non_ace)
    assert hand.score() == 31

def test_soft_false(hand: BlackjackHand, non_ace: Card):
    """no aces is hard"""
    hand.append(non_ace)
    assert not hand.soft()

def test_soft_ace_eleven(ace: Card, hand: BlackjackHand):
    """ace 11 is soft"""
    hand.append(ace)
    assert hand.soft()

def test_soft_ace_one(
    ace: Card,
    hand: BlackjackHand,
    non_ace: Card,
):
    """ace 1 is hard"""
    hand.append(ace)
    hand.append(non_ace)
    hand.append(non_ace)
    assert not hand.soft()

def test_split(
    ace: Card,
    hand: BlackjackHand,
    non_ace: Card,
):
    """splits hand into two"""
    hand.append(ace)
    hand.append(non_ace)
    other_hand = hand.split()
    assert len(hand) == 1
    assert other_hand[0] == non_ace

def test_split_error(hand: BlackjackHand):
    """splitting on non size 2 hand raises error"""
    with pytest.raises(IndexError):
        hand.split()
