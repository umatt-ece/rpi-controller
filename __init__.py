"""
Package: rpi-controller
Purpose: Root Python package for the project. This file also contains the logging configurations for all loggers used
         throughout the various modules.
"""
import logging.config
import logging


# configure formatters, handlers, and loggers for the project
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(filename)s | %(levelname)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "hardware_file_handler": {
            "class": "logging.FileHandler",
            "filename": "log/hardware.log",
            "formatter": "default",
        },
        "logic_file_handler": {
            "class": "logging.FileHandler",
            "filename": "log/logic.log",
            "formatter": "default",
        }
    },
    "loggers": {
        "hardware": {
            "level": "INFO",
            "handlers": ["console", "hardware_file_handler"],
        },
        "logic": {
            "level": "INFO",
            "handlers": ["console", "logic_file_handler"],
        },
        "controller": {
            "level": "ERROR",
            "handlers": ["console"],
        },
    }
})
