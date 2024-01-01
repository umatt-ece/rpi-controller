"""
Package: rpi-controller
Purpose: Root Python package for the project. This file also contains the logging configurations for all loggers used
         throughout the various modules.
"""
import logging.config
import logging
from datetime import datetime

import common  # Required that 'common' be imported first (for dependency injection)


# configure formatters, handlers, and loggers for the project
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(filename)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": f"log/{datetime.now().strftime('%Y-%m-%d')}.log",
            "formatter": "default",
        },
    },
    "loggers": {
        "database": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
        },
        "server": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
        },
        "hardware": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
        },
        "logic": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
        },
        "controller": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
        },
    }
})
