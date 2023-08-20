"""test face values"""
# Date:	13 Aug 2023
# Revision History:
#	resultay | 13-08-23 | Initial version

from src.constants.suit import Suit

def test_values():
    """test values"""
    values = set(suit.value for suit in Suit)
    assert values == set([
		'\u2663', '\u2666',
        '\u2665', '\u2660'
    ])
