"""test games utility functions"""
# Date:	02 Dec 2023
# Revision History:
#	resultay | 02-12-23 | Initial version

import random
import sys
from src.general import games

def test_set_seed():
    """generates random seed"""
    random.seed(104)
    seed = games.set_seed()
    assert seed == 180164991607898107

def test_set_specific_seed():
    """sets with given seed"""
    expected_seed = random.randrange(sys.maxsize)
    actual_seed = games.set_seed(expected_seed)
    assert actual_seed == expected_seed
