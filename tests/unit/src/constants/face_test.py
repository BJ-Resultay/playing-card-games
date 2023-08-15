"""test face values"""
# Date:	13 Aug 2023
# Revision History:
#	resultay | 13-08-23 | Initial version

from constants import Face

def test_values():
    """test values"""
    values = set(face.value for face in Face)
    assert values == set([
		'A', '2', '3', '4', '5',
		'6', '7', '8', '9', '10',
		'J', 'Q', 'K'
    ])
