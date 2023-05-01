from collections import namedtuple
from enum import Enum


class StoredData(namedtuple("storedData", "datatype default"), Enum):
    """
    ...
    """

    INITIALIZED = (
        bool,
        True,
    )

    ACC_POWER = (
        bool,
        True,
    )

    BOUNCE_TIME_THRESHOLD_N = (
        int,
        1,
    )

    BOUNCE_TIME_THRESHOLD = (
        int,
        1,
    )

    MOTOR_ENABLE_SUCCESS = (
        bool,
        False,
    )

    ACCEPTABLE_JOYSTICK_MAPS = (
        list,
        [0],
    )

    ACCELERATION_MAX = (
        int,
        1,
    )

    ACCELERATION_MIN = (
        int,
        1,
    )

    DIFF_MIN_TIME = (
        float,
        0.5,
    )

    # PULL_MODE_THRESHOLD = (
    #     float,
    #     1.0,  # arbitrary for rn
    #     "unknown",
    # )

    MACHINE_HOURS = (
        float,
        0.0,
    )

