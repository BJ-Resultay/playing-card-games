"""test blackjack bot ai"""
# Date:	28 Sep 2023
# Revision History:
#	resultay | 28-09-23 | Initial version

from pytest_mock import MockerFixture
import pytest
from src.games.blackjack.blackjack_bot import BlackjackBot
from src.games.blackjack.blackjack_deck import BlackjackDeck
from src.games.blackjack.constants import BlackjackError
from src.general import Face
from src.general.card import Card

def should_double_down(
    card: Card,
    mask: list[int],
) -> None:
    """test_should_double_down helper"""
    bot = BlackjackBot('David Blaine')
    bot.add_card(card)
    for i in range(2, 12):
        if i in mask:
            assert bot.should_double_down(i)
        else:
            assert not bot.should_double_down(i)

@pytest.mark.parametrize(
    'points, mask',
    [
        (13, [5, 6]),
        (14, [5, 6]),
        (15, range(4, 7)),
        (16, range(4, 7)),
        (17, range(3, 7)),
        (18, range(2, 7)),
        (19, [6]),
        (20, []),
        (21, []),
    ]
)
def test_should_double_down_soft(
    ace: Card,
    mask: list[int],
    points: int,
):
    """bot should double down with soft hand"""
    # Soft 19 doubles against dealer 6
    # Soft 18 doubles against dealer 2 through 6
    # Soft 17 doubles against dealer 3 through 6
    # Soft 16 doubles against dealer 4 through 6
    # Soft 15 doubles against dealer 4 through 6
    # Soft 14 doubles against dealer 5 through 6
    # Soft 13 doubles against dealer 5 through 6
    ace.points = points
    should_double_down(ace, mask)

should_not_double_down_hard_param = [
    pytest.param(i, [])
    for i in range(9, 22)
    if i not in range(2, 12)
]

@pytest.mark.parametrize(
    'points, mask',
    [
        (10, range(2, 10)),
        (11, range(2, 12)),
        (9, range(3, 7)),
    ] + should_not_double_down_hard_param
)
def test_should_double_down_hard(
    mask: list[int],
    non_ace: Card,
    points: int,
):
    """bot should double down with hard hand"""
    # Hard 11 always doubles.
    # Hard 10 doubles against dealer 2 through 9
    # Hard 9 doubles against dealer 3 through 6
    non_ace.points = points
    should_double_down(non_ace, mask)

should_not_split_param = [
    pytest.param(face, [])
    for face in [Face.TEN, Face.FIVE, Face.JACK, Face.KING, Face.QUEEN]
]

@pytest.mark.parametrize(
    'face, mask',
    [
        (Face.ACE, range(2, 12)),
        (Face.EIGHT, range(2, 12)),
        (Face.FOUR, [5, 6]),
        (Face.NINE, list(range(2, 7)) + [8, 9]),
        (Face.SEVEN, range(2, 8)),
        (Face.SIX, range(2, 7)),
        (Face.THREE, range(2, 8)),
        (Face.TWO, range(2, 8)),
    ] + should_not_split_param
)
def test_should_split(
    face: Face,
    mask: list[int],
    bot: BlackjackBot,
):
    """bot should split"""
    # Always split As
    # 9s splits against dealer 2 through 9, not 7
    # Always split 8s
    # 7s splits against dealer 2 through 7
    # 6s splits against dealer 2 through 6
    # 4s splits against dealer 5 and 6
    # 3s splits against dealer 2 through 7
    # 2s splits against dealer 2 through 7
    card = Card(face, None)
    bot.add_card(card)
    bot.add_card(card)
    for i in range(2, 12):
        if i in mask:
            assert bot.should_split(i)
        else:
            assert not bot.should_split(i)

def test_should_stand18(
    ace: Card,
    bot: BlackjackBot
):
    """bot should not stand with soft 18 against dealer 9 through Ace"""
    bot.add_card(ace)
    ace.points = 18
    for i in range(2, 9):
        assert bot.should_stand(i)
    for i in range(9, 12):
        assert not bot.should_stand(i)

def test_should_stand(
    non_ace: Card,
    bot: BlackjackBot
):
    """bot should stand with 17+"""
    bot.add_card(non_ace)
    for i in range(17, 22):
        non_ace.points = i
        for j in range(9, 12):
            assert bot.should_stand(j)

def test_should_not_stand(
    non_ace: Card,
    bot: BlackjackBot
):
    """bot should not stand with 16-"""
    bot.add_card(non_ace)
    for i in range(4, 17):
        non_ace.points = i
        for j in range(9, 12):
            assert not bot.should_stand(j)

def test_should_surrender15(
    non_ace: Card,
    bot: BlackjackBot
):
    """bot should surrender with 15 against dealer 10"""
    bot.add_card(non_ace)
    non_ace.points = 15
    assert bot.should_surrender(10)
    for i in range(2, 12):
        if i == 10:
            continue
        assert not bot.should_surrender(i)

def test_should_surrender16(
    non_ace: Card,
    bot: BlackjackBot
):
    """bot should surrender with 15 against dealer 9 through Ace"""
    bot.add_card(non_ace)
    non_ace.points = 16
    for i in range(9, 12):
        assert bot.should_surrender(10)
    for i in range(2, 9):
        assert not bot.should_surrender(i)

def test_should_not_surrender(
    non_ace: Card,
    bot: BlackjackBot
):
    """bot should not surrender otherwise"""
    bot.add_card(non_ace)
    for i in range(4, 22):
        if i in [15, 16]:
            continue
        assert not bot.should_surrender(i)

def test_turn(
    ace: Card,
    bot: BlackjackBot,
    deck: BlackjackDeck,
    mocker: MockerFixture,
    non_ace: Card,
):
    """bot splits, doubles down, and hits, then stands"""
    mocker.patch.object(bot, 'can_surrender', return_value = False)
    mocker.patch.object(bot, 'can_split', side_effect = [True, True, False, False, False])
    mocker.patch.object(bot, 'can_double_down', side_effect = [True, True, False, False])
    mocker.patch.object(bot, 'can_stand', side_effect = [False, True, True])
    mocker.patch.object(bot, 'can_hit', return_value = True)
    mocker.patch.object(bot, 'should_split', return_value = True)
    mocker.patch.object(bot, 'should_double_down', return_value = True)
    mocker.patch.object(bot, 'should_stand', return_value = True)
    mocker.patch.object(deck, 'draw', return_value = non_ace)
    split = mocker.spy(bot, 'split')
    double_down = mocker.spy(bot, 'double_down')
    hit = mocker.spy(bot, 'hit')
    stand = mocker.spy(bot, 'stand')

    bot.hand.append(ace)
    bot.hand.append(ace)
    bot.turn(0, deck)
    split.assert_called_once_with(non_ace, non_ace)
    double_down.assert_called_once_with(non_ace)
    hit.assert_called_once_with(non_ace)
    stand.assert_called_once()

def test_turn_surrender(
    bot: BlackjackBot,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """bot surrenders"""
    mocker.patch.object(bot, 'can_surrender', return_value = True)
    mocker.patch.object(bot, 'should_surrender', return_value = True)
    surrender = mocker.spy(bot, 'surrender')

    bot.turn(0, deck)
    surrender.assert_called_once()

def test_turn_error(
    bot: BlackjackBot,
    deck: BlackjackDeck,
    mocker: MockerFixture,
):
    """bot has no moves"""
    mocker.patch.object(bot, 'can_surrender', return_value = False)
    mocker.patch.object(bot, 'can_split', return_value = False)
    mocker.patch.object(bot, 'can_double_down', return_value = False)
    mocker.patch.object(bot, 'can_stand', return_value = False)
    mocker.patch.object(bot, 'can_hit', return_value = False)

    with pytest.raises(BlackjackError):
        bot.turn(0, deck)
