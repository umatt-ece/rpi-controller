import enum
from collections import namedtuple

"""
NOTE: when adding new values to this enum, you will likely need to flush the Redis database so that the new values can
be initialized properly. To do this, with the redis container running in docker use the following command. You may need
to change 'rpi-controller_database_1' depending on how exactly docker names your containers on startup.

docker exec -it rpi-controller_database_1 redis-cli FLUSHALL
"""


class LiveData(namedtuple("live_data", "datatype default"), enum.Enum):
    """
    ...
    """

    TEST_PARAM = (
        bool,
        True,
    )

    INITIALIZED = (
        bool,
        True,
    )

    CONTROLLER_ONLINE = (
        bool,
        False,
    )

    INCHING = (
        bool,
        False,
    )

    BRAKE = (
        bool,
        False,
    )

    CLUTCH = (
        bool,
        False,
    )

    THROTTLE = (
        bool,
        False,
    )

    ENABLE_MOTOR = (
        bool,
        False,
    )

    FORWARDS = (
        bool,
        False,
    )

    REVERSE = (
        bool,
        False,
    )

    NEUTRAL = (
        bool,
        True,
    )

    GEAR_LOCKOUT = (
        list,
        [False, False],
    )

    FANS = (
        bool,
        False,
    )

    PUMP = (
        bool,
        False,
    )

    LA_EXTEND = (
        bool,
        False,
    )

    LA_RETRACT = (
        bool,
        False,
    )

    BOUNCE_TIMER = (
        bool,
        False,
    )

    DIFF_SPEED = (
        bool,
        False,
    )

    MODE_MANEUVERABILITY = (
        bool,
        True,
    )

    MODE_PULLING = (
        bool,
        False,
    )

    DIFF_LOCK_REQUEST = (
        bool,
        False,
    )

    JOYSTICK_MAPPING = (
        int,
        0,  # 0 = linear
    )

    ACCELERATION = (
        int,
        0,  # 0 = no limitation
    )

    DECELERATION = (
        int,
        0,  # 0 = no limitation
    )

    INTERLOCK_OVERRIDE = (
        bool,
        False,
    )


    # SPEED = (
    #     float,
    #     0.0,
    #     "km/h",
    # )
    #
    # RPM = (
    #     float,
    #     0.0,
    #     "RPM",
    # )
    #
    # GEAR = (
    #     int,
    #     0,
    #     "unitless",
    # )
    #
    # OIL_TEMP = (
    #     float,
    #     0.0,
    #     "unitless",
    # )
    #
    # ELECTRIC_MOTOR_POWER = (
    #     float,
    #     0.0,
    #     "unitless",
    # )
    #
    # DIFFERENTIAL_SPEED = (
    #     float,
    #     0.0,
    #     "unitless",
    # )
    #
    # BATTERY_VOLTAGE = (
    #     float,
    #     0.0,
    #     "unitless",
    # )
    #
    # TURN_SIGNAL_LEFT = (
    #     bool,
    #     False,
    #     "unitless",
    # )
    #
    # TURN_SIGNAL_RIGHT = (
    #     bool,
    #     False,
    #     "unitless",
    # )
    #
    # TOW_MODE_LOCK = (
    #     bool,
    #     False,
    #     "unitless",
    # )
    #
    # HEADLIGHTS = (
    #     bool,
    #     False,
    #     "unitless",
    # )
    #
    # DIFFERENTIAL_LOCK = (
    #     bool,
    #     False,
    #     "unitless",
    # )
