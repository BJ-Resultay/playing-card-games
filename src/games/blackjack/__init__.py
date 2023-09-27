"""modules in blackjack package"""
import logging.config
from src.general import LOG_CONFIG

from .main import main

logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
"""logger for blackjack classes"""

__all__ = [
    'main',
]
