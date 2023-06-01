import enum
from collections import namedtuple

"""
NOTE: when adding new values to this enum, you will likely need to flush the Redis database so that the new values can
be initialized properly. To do this, with the redis container running in docker use the following command. You may need
to change 'rpi-controller_database_1' depending on how exactly docker names your containers on startup.

docker exec -it rpi-controller_database_1 redis-cli FLUSHALL
"""


class Parameters(namedtuple("parameter", "datatype default"), enum.Enum):
    """
    ...
    """

    INITIALIZED = (
        bool,
        True,
    )

    HEADLIGHT_LEFT = (
        bool,
        False,
    )
    HEADLIGHT_RIGHT = (
        bool,
        False,
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

    DIFF_UNLOCK_REQUEST = (
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

    SPEED = (
        float,
        0.0,
    )
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

    POWER_DOWN = (
        bool,
        False,
    )

