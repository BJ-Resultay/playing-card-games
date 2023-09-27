"""modules in general package"""

import logging.config
from .face import Face
from .suit import Suit

LOG_CONFIG = 'logging.ini'
"""logging config for getLogger"""

logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
"""logger for general classes"""

__all__ = [
    'Face',
    'Suit',
]
