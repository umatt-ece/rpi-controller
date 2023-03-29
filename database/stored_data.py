from collections import namedtuple
from enum import Enum


class StoredData(namedtuple("storedData", "datatype default unit"), Enum):
    """
    ...
    """

    INITIALIZED = (
        bool,
        True,
        "unitless",
    )

    PULL_MODE_THRESHOLD = (
        float,
        1.0,  # arbitrary for rn
        "unknown",
    )

    MACHINE_HOURS = (
        float,
        0.0,
        "hours",
    )

