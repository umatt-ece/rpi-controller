"""
This file contains a python dictionaries of all entries to be stored in Redis (live/stored values). When added new
entries, please adhere to the following:

- All entry names should be in snake_case
- All entries must contain a tuple with the following 4 values:
    - datatype
    - default value
    - unit of measurement ("unitless" if no units)
    - description
"""


class LiveData:
    parameter_type = "LiveData"

    def __init__(self, key: str, datatype, default, unit: str, description: str):
        self.key = key
        self.datatype = datatype
        self.default = default
        self.unit = unit
        self.description = description


class StoredData:
    parameter_type = "StoredData"

    def __init__(self, key: str, datatype, default, unit: str, description: str):
        self.key = key
        self.datatype = datatype
        self.default = default
        self.unit = unit
        self.description = description


live_data = (
    LiveData(
        "initialized",
        bool,
        False,
        "unitless",
        "flag to determine if the redis live database has been initialized yet",
    ),
    LiveData(
        "speed",
        float,
        0.0,
        "km/h",
        "speed of the tractor.",
    ),
)

stored_data = (
    StoredData(
        "initialized",
        bool,
        False,
        "unitless",
        "flag to determine if the redis live database has been initialized yet",
    ),
)




#     "initialized": (
#         bool,
#         False,
#         "unitless",
#         "flag to determine if the redis live database has been initialized yet"
#     ),
#     "speed": (
#         float,
#         0.0,
#         "km/h",
#         "speed of the tractor.",
#     ),
#     "rpm": (
#         float,
#         0.0,
#         "RPM",
#         "rotational speed of the motor.",
#     ),
#     "gear": (
#         int,
#         0,
#         "unitless",
#         "transmission state (park, reverse, drive, tow)."
#     )
# }
#
# stored_data = {
#     "initialized": (
#         bool,
#         False,
#         "unitless",
#         "flag to determine if the redis stored database has been initialized yet"
#     ),
#     "pull_mode_threshold": (
#         float,
#         1.0,  # TODO: arbitrary for rn, need to fix
#         "unknown",
#         "threshold at which the tractor transitions from drive -> tow mode.",
#     ),
#     "machine_hours": (
#         float,
#         0.0,
#         "hours",
#         "time that the control system has run since it's installation.",
#     ),
#     "oil_temp": (
#         float,
#         0.0,
#         "",
#         "",
#     ),
#     "electric_motor_power": (
#         float,
#         0.0,
#         "",
#         "",
#     ),
#     "differential_speed": (
#         float,
#         0.0,
#         "",
#         "",
#     ),
#
#     "battery_voltage": (
#         float,
#         0.0,
#         "",
#         "",
#     ),
#     "turn_signal_left": (
#         bool,
#         False,
#         "",
#         "",
#     ),
#     "turn_signal_right": (
#         bool,
#         False,
#         "",
#         "",
#     ),
#     "tow_mode_lock": (
#         bool,
#         False,
#         "",
#         "",
#     ),
#     "headlights": (
#         bool,
#         False,
#         "",
#         "",
#     ),
#     "differential_lock": (
#         bool,
#         False,
#         "",
#         "",
#     ),
# }
#
#
# def snake_to_camel(string: str):
#     return string.split('_')[0] + ''.join(x.capitalize() for x in string.split('_')[1:])
