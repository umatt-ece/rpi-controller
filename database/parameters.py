import enum
from collections import namedtuple

"""
NOTE: when adding new values to this enum, you will likely need to flush the Redis database so that the new values can
be initialized properly. To do this, with the redis container running in docker use the following command. You may need
to change 'rpi-controller_database_1' depending on how exactly docker names your containers on startup.

docker exec -it rpi-controller_database_1 redis-cli FLUSHALL
"""


class Parameters(namedtuple("parameter", "datatype default description"), enum.Enum):
    """
    ...
    """

    INITIALIZED = (
        bool,
        True,
        "init",
    )

    HEADLIGHT_LEFT = (
        bool,
        False,
        "head_l",
    )
    HEADLIGHT_RIGHT = (
        bool,
        False,
        "head_r",
    )

    CONTROLLER_ONLINE = (
        bool,
        False,
        "contr_online",
    )

    # INCHING = (
    #     bool,
    #     False,
    # )

    # BRAKE = (
    #     bool,
    #     False,
    # )

    # CLUTCH = (
    #     bool,
    #     False,
    # )

    # THROTTLE = (
    #     bool,
    #     False,
    # )
    #
    # ENABLE_MOTOR = (
    #     bool,
    #     False,
    # )

    # FORWARDS = (
    #     bool,
    #     False,
    # )
    #
    # REVERSE = (
    #     bool,
    #     False,
    # )
    #
    # NEUTRAL = (
    #     bool,
    #     True,
    # )
    #
    # FANS = (
    #     bool,
    #     False,
    # )
    #
    # PUMP = (
    #     bool,
    #     False,
    # )
    #
    # LA_EXTEND = (
    #     bool,
    #     False,
    # )
    #
    # LA_RETRACT = (
    #     bool,
    #     False,
    # )

    # BOUNCE_TIMER = (
    #     bool,
    #     False,
    # )

    DIFF_SPEED = (
        bool,
        False,
        "diff_speed",
    )

    MODE_MANEUVERABILITY = (
        bool,
        True,
        "mode_maneuverability",
    )

    MODE_PULLING = (
        bool,
        False,
        "mode_pulling",
    )

    DIFF_LOCK_REQUEST = (
        bool,
        False,
        "diff_lock_request",
    )

    DIFF_UNLOCK_REQUEST = (
        bool,
        False,
        "diff_unlock_request",
    )

    # JOYSTICK_MAPPING = (
    #     int,
    #     0,  # 0 = linear
    # )

    ACCELERATION = (
        int,
        0,  # 0 = no limitation
        "acc",
    )

    DECELERATION = (
        int,
        0,  # 0 = no limitation
        "decel",
    )

    INTERLOCK_OVERRIDE = (
        bool,
        False,
        "interlock_override",
    )


    SPEED = (
        float,
        0.0,
        "speed",
    )

    RPM = (
        float,
        0.0,
        "rpm",
    )

    GEAR = (
        int,
        0,
        "gear",
    )

    OIL_TEMP = (
        float,
        0.0,
        "oil_temp",
    )

    OIL_PRESSURE = (
        float,
        0.0,
        "oil_pressure",
    )

    # ELECTRIC_MOTOR_POWER = (
    #     float,
    #     0.0,
    #     # "unitless",
    # )

    DIFFERENTIAL_SPEED = (
        float,
        0.0,
        "differential_speed",
    )

    GSL_POSITION = (
        float,
        0.0,
        "gsl",
    )

    # BATTERY_VOLTAGE = (
    #     float,
    #     0.0,
    #     # "unitless",
    # )

    TURN_SIGNAL_LEFT = (
        bool,
        False,
        "turn_signal_l",
    )

    TURN_SIGNAL_RIGHT = (
        bool,
        False,
        "turn_signal_r",
    )

    TOW_MODE_LOCK = (
        bool,
        False,
        "tow_mode_lock",
    )

    # HEADLIGHTS = (
    #     bool,
    #     False,
    #     # "unitless",
    # )

    DIFFERENTIAL_LOCK = (
        bool,
        False,
        "differential_lock",
    )

    # ACC_POWER = (
    #     bool,
    #     True,
    # )

    # BOUNCE_TIME_THRESHOLD_N = (
    #     int,
    #     1,
    # )
    #
    # BOUNCE_TIME_THRESHOLD = (
    #     int,
    #     1,
    # )

    # MOTOR_ENABLE_SUCCESS = (
    #     bool,
    #     False,
    # )

    ACCELERATION_MAX = (
        int,
        1,
        "acc_max",
    )

    ACCELERATION_MIN = (
        int,
        1,
        "acc_min",
    )

    # DIFF_MIN_TIME = (
    #     float,
    #     0.5,
    # )

    # PULL_MODE_THRESHOLD = (
    #     float,
    #     1.0,  # arbitrary for rn
    #     # "unknown",
    # )

    MACHINE_HOURS = (
        float,
        0.0,
        "hours",
    )

    POWER_DOWN = (
        bool,
        False,
        "power_down",
    )

