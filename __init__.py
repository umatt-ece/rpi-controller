"""
Package: rpi-controller
Purpose: Root Python package for the project. This file also contains the logging configurations for all loggers used
         throughout the various modules.
"""
import logging.config
import logging
from datetime import datetime

import common  # 'common' must be imported first (for dependency injection)
from common import logging_config

# configure formatters, handlers, and loggers for the project
logging.config.dictConfig(logging_config)
