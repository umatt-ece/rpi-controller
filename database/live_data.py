from collections import namedtuple
from enum import Enum


class LiveData(namedtuple("live_data", "datatype unit description"), Enum):
    """
    ...
    """

    SPEED = (
        float,
        "km/h",
        "speed of the tractor.",
    ),

    RPM = (
        float,
        "RPM",
        "rotational speed of the motor.",
    ),

    GEAR = (
        int,
        "unitless",
        "transmission state (park, reverse, drive, tow)."
    ),

    OIL_TEMP = (
        float,
        "",
        "",
    ),

    ELECTRIC_MOTOR_POWER = (
        float,
        "",
        "",
    ),

    DIFFERENTIAL_SPEED = (
        float,
        "",
        "",
    ),

    BATTERY_VOLTAGE = (
        float,
        "",
        "",
    ),

    TURN_SIGNAL_LEFT = (
        bool,
        "",
        "",
    ),

    TURN_SIGNAL_RIGHT = (
        bool,
        "",
        "",
    ),

    TOW_MODE_LOCK = (
        bool,
        "",
        "",
    ),

    HEADLIGHTS = (
        bool,
        "",
        "",
    ),

    DIFFERENTIAL_LOCK = (
        bool,
        "",
        "",
    ),


