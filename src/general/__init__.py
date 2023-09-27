"""modules in general package"""

import logging.config
from src.constants import LOG_CONFIG

logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
"""logger for general classes"""
