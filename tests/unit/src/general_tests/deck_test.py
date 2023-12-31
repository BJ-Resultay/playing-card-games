"""test deck"""
# Date:	18 Aug 2023
# Revision History:
#	resultay | 18-08-23 | Initial version

import random
import pytest
from src.general import Face
from src.general import Suit
from src.general.card import Card
from src.general.deck import Deck

@pytest.fixture()
def deck() -> Deck:
    """fixture returns standard deck"""
    return Deck()

@pytest.fixture()
def card() -> Card:
    """fixture returns queen of hearts"""
    return Card(Face.QUEEN, Suit.HEART) # position 11

@pytest.fixture(autouse = True)
def seed() -> None:
    """set fixed seed"""
    return random.seed(52)

def test_ace_spade(deck: Deck):
    """last card of standard deck is ace of spades"""
    assert deck.order[-1] == Card(Face.ACE, Suit.SPADE)

def test_not_ace_spade(card: Card):
    """last card of non standard deck is custom"""
    deck = Deck([card])
    assert deck.order[-1] == card

def test_addition(deck: Deck):
    """decks are added together"""
    deck2 = deck + deck
    assert len(deck2.order) == 104

def test_multiplication(deck: Deck):
    """decks multiply deck first"""
    deck2 = deck * 3
    assert len(deck2.order) == 156

def test_reverse_multiplication(deck: Deck):
    """decks multiply int first"""
    deck2 = 5 * deck
    assert len(deck2.order) == 260

def test_add_card(deck: Deck, card: Card):
    """custom card is added to the end of the deck"""
    deck.add_card(card)
    assert deck.order[-1] == card

def test_add_card_error(deck: Deck):
    """adding non card raises error"""
    with pytest.raises(AttributeError):
        deck.add_card('not card')

def test_deal(deck: Deck, card: Card):
    """returns card and removes from deck"""
    assert len(deck.order) == 52
    deck_card = deck.deal(11)
    assert deck_card == card
    assert len(deck.order) == 51

def test_deal_empty(deck: Deck):
    """empty deck raises error"""
    deck.order = []
    with pytest.raises(AttributeError):
        deck.deal()

def test_deal_not_int(deck: Deck):
    """not passing int raises error"""
    with pytest.raises(AttributeError):
        deck.deal('53')

def test_deal_not_in_range(deck: Deck):
    """int not in range raises error"""
    # -len(deck.order) == 0
    with pytest.raises(AttributeError):
        deck.deal(52)

def test_face_values(deck: Deck, card: Card):
    """returns face values"""
    assert card.face_value() in deck.face_values()

def test_false_shuffle(deck: Deck, card: Card):
    """card ends up on top"""
    deck.false_shuffle([11])
    deck_card = deck.deal()
    assert deck_card == card

def test_false_shuffle_garbage(deck: Deck, card: Card):
    """garbage does not have side effects"""
    deck.false_shuffle([11, 'garbage'])
    deck_card = deck.deal()
    assert deck_card == card

def test_false_shuffle_not_list(deck: Deck):
    """not list indexes raises error"""
    with pytest.raises(AttributeError):
        deck.false_shuffle('11')

def test_false_shuffle_too_long(deck: Deck):
    """indexes longer than deck raises error"""
    indexes = [None] * 53
    assert len(deck.order) == 52
    with pytest.raises(AttributeError):
        deck.false_shuffle(indexes)

def test_flip(deck: Deck):
    """reverses order and flips all cards"""
    deck.flip()
    card = deck.deal()
    assert card == Card(Face.ACE, Suit.SPADE)
    assert not card.face_down

def test_remove_cards(deck: Deck, card: Card):
    """remove cards in list"""
    deck.add_card(card)
    removed_cards = deck.remove_cards([card])
    assert removed_cards == [card, card]

def test_remove_cards_either(deck: Deck, card: Card):
    """remove cards of face/suit/point"""
    deck.remove_cards_either(suit = card.suit)
    assert card not in deck.order

def test_reverse(deck: Deck):
    """reverses order without flipping cards"""
    deck.reverse()
    card = deck.deal()
    assert card == Card(Face.ACE, Suit.SPADE)
    assert card.face_down

def test_shuffle(deck: Deck):
    """randomly shuffles"""
    # autouse seed fixture
    deck.shuffle()
    card = deck.deal()
    assert card == Card(Face.KING, Suit.SPADE)
