from collections import namedtuple
import enum

"""
This file contains a python dictionary of all entries to be stored in Redis (live values). When added new entries,
please adhere to the following:

- All entry names are in ALL_CAPS_SNAKE_CASE
- All entries must contain a tuple with the following 4 values:
    - datatype
    - default value
    - unit of measurement ("unitless" if no units)
    - description
"""

live_data = {
    "initialized": (
        bool,
        False,
        "unitless",
        "flag to determine if the redis database has been initialized yet"
    )
}

class LiveData(namedtuple("live_data", "datatype default unit description"), enum.Enum):
    """
    ...
    """

    INITIALIZED = (
        bool,
        False,
        "unitless",
        "flag to determine if the redis database has been initialized yet"
    )

    SPEED = (
        float,
        0.0,
        "km/h",
        "speed of the tractor.",
    )

    RPM = (
        float,
        0.0,
        "RPM",
        "rotational speed of the motor.",
    )

    GEAR = (
        int,
        0,
        "unitless",
        "transmission state (park, reverse, drive, tow)."
    )

    OIL_TEMP = (
        float,
        0.0,
        "",
        "",
    )

    ELECTRIC_MOTOR_POWER = (
        float,
        0.0,
        "",
        "",
    )

    DIFFERENTIAL_SPEED = (
        float,
        0.0,
        "",
        "",
    )

    BATTERY_VOLTAGE = (
        float,
        0.0,
        "",
        "",
    )

    TURN_SIGNAL_LEFT = (
        bool,
        False,
        "",
        "",
    )

    TURN_SIGNAL_RIGHT = (
        bool,
        False,
        "",
        "",
    )

    TOW_MODE_LOCK = (
        bool,
        False,
        "",
        "",
    )

    HEADLIGHTS = (
        bool,
        False,
        "",
        "",
    )

    DIFFERENTIAL_LOCK = (
        bool,
        False,
        "",
        "",
    )
