"""module initializes general constants"""
# Date:	27 Sep 2023
# Revision History:
#	resultay | 27-09-23 | Initial version

import logging.config
from src.constants import LOG_CONFIG

logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
LOGGER = logging.getLogger('general')
"""logger for general classes"""
