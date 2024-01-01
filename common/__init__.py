"""
Package: Common
Purpose: This package contains code used by all modules of the project, helping to reduce the amount of repeated
         code fragments.
"""
from datetime import datetime

from .utils import validate_binary_string, swap_string_endian, integer_to_binary_string, binary_string_to_integer
from .dependency_handler import get_data_store, get_client_manager, get_raspberry_pi

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(name)-14s | %(levelname)-5s | %(filename)-21s | %(message)s",
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
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console", "file_handler"],
        },
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
}