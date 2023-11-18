"""module contains helpful game functions"""
# Date:	17 Nov 2023
# Revision History:
#	resultay | 17-11-23 | Initial version

from logging import getLogger
import random
import sys

LOGGER = getLogger(__name__)

def set_seed(seed: int = None) -> int:
    """set random seed

    Args:
        seed (int, optional): sets randomness. Defaults to random in sys maxsize.

    Returns:
        int: seed set
    """
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return seed
