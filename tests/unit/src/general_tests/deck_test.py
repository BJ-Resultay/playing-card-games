"""test deck"""
# Date:	18 Aug 2023
# Revision History:
#	resultay | 18-08-23 | Initial version

import random
import pytest
from src.constants import Face
from src.constants import Suit
from src.general import Card
from src.general import Deck

@pytest.fixture()
def deck():
    """fixture returns standard deck"""
    return Deck()
