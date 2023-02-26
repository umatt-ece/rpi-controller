from collections import namedtuple
from enum import Enum


class StoredData(namedtuple("storedData", "datatype default unit description"), Enum):
    """
    ...
    """

    PULL_MODE_THRESHOLD = (
        float,
        1.0,  # arbitrary for rn
        "unknown",
        "threshold at which the tractor transitions from drive -> tow mode.",
    ),

    MACHINE_HOURS = (
        float,
        0.0,
        "hours",
        "time that the control system has run since it's installation.",
    ),
