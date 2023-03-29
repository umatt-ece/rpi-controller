from collections import namedtuple
import enum


class LiveData(namedtuple("live_data", "datatype default unit"), enum.Enum):
    """
    ...
    """

    INITIALIZED = (
        bool,
        True,
        "unitless",
    )

    CONTROLLER_ONLINE = (
        bool,
        False,
        "unitless",
    )

    SPEED = (
        float,
        0.0,
        "km/h",
    )

    RPM = (
        float,
        0.0,
        "RPM",
    )

    GEAR = (
        int,
        0,
        "unitless",
    )

    OIL_TEMP = (
        float,
        0.0,
        "unitless",
    )

    ELECTRIC_MOTOR_POWER = (
        float,
        0.0,
        "unitless",
    )

    DIFFERENTIAL_SPEED = (
        float,
        0.0,
        "unitless",
    )

    BATTERY_VOLTAGE = (
        float,
        0.0,
        "unitless",
    )

    TURN_SIGNAL_LEFT = (
        bool,
        False,
        "unitless",
    )

    TURN_SIGNAL_RIGHT = (
        bool,
        False,
        "unitless",
    )

    TOW_MODE_LOCK = (
        bool,
        False,
        "unitless",
    )

    HEADLIGHTS = (
        bool,
        False,
        "unitless",
    )

    DIFFERENTIAL_LOCK = (
        bool,
        False,
        "unitless",
    )

