"""module initializes blackjack constants"""
# Date:	14 Sep 2023
# Revision History:
#	resultay | 14-09-23 | Initial version

import logging.config
from src.constants import LOG_CONFIG

BLACKJACK = 'blackjack'

logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
LOGGER = logging.getLogger(BLACKJACK)
"""logger for blackjack classes"""

class BlackjackError(Exception):
    """error class for blackjack"""
