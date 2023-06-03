import math
import time
import enum

from controller import GpioHandler, Expander, Potentiometer, AnalogDigitalConverter, RpiPin as Pin, binary_to_decimal
from database import DataStore, Parameters

# TODO: create functions for state machine logic, break up into 'states'/'transitions'
# TODO: further abstraction, drive_state_machine.py should be purely logic, no reference to specific GPIO pins


class DriveState(enum.Enum):
    PARK = "PARK"
    REVERSE = "REVERSE"
    NEUTRAL = "NEUTRAL"
    FORWARD = "FORWARD"


class DriveStateMachine:
    _acc_pwr = 1

    _bounce_time_thresh_n = 1
    _bounce_time_thresh = 1

    _motor_enable_success = 0

    _acceptable_joystick_maps = [0]
    _acceleration_max = 1
    _acceleration_min = 1
    _diff_min_time = 0.5

    def __init__(self):
        self._data_store = DataStore()
        self._gpio = GpioHandler()
        self._xpndr = Expander()
        self._pot = Potentiometer()
        self._adc = AnalogDigitalConverter()

        self._state = DriveState.PARK

        # internally calculated
        self.inching = 0
        self.brake = 0
        self.clutch = 0
        self.throttle = 0
        self.enable_motor = 0
        self.forward = 0
        self.reverse = 0
        self.neutral = 1
        self.gear_lockout = [0, 0]
        self.fan = 0
        self.pump = 0
        self.la_extend = 0
        self.la_retract = 0
        self.bounce_timer = 0
        self.diff_speed = 0

        # externally set
        self.mode_maneuverability = 1
        self.mode_pulling = 0
        self.diff_lock_request = 0
        self.joystick_mapping = 0  # 0 = linear
        self.acceleration = 0  # 0 = no limitation
        self.deceleration = 0  # 0 = no limitation
        self.interlock_override = 0

        self._last_runtime_diff = time.perf_counter()
        self._last_runtime = time.perf_counter()

    def initialize(self):
        self._xpndr.write_gpio(3, "A", [1, 1, 1, 1, 1, 1, 1, 1])
        self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 0, 0])

    def update_values(self):
        if self._data_store.get(Parameters.MODE_MANEUVERABILITY):  # set to maneuverability
            if self._state == DriveState.NEUTRAL:
                self.mode_maneuverability = 1
                self.mode_pulling = 0
            self._data_store.set(Parameters.MODE_MANEUVERABILITY, False)

        if self._data_store.get(Parameters.MODE_PULLING):  # set to pulling
            if self._state == DriveState.NEUTRAL:
                self.mode_maneuverability = 0
                self.mode_pulling = 1
            self._data_store.set(Parameters.MODE_PULLING, False)

        # if self._data_store.get(Parameters.DIFF_LOCK_REQUEST):  # set difflock
        #     if self._state == DriveState.NEUTRAL:
        #         self.diff_lock_request = 1
        #     self._data_store.set(Parameters.DIFF_LOCK_REQUEST, False)

        # if self._data_store.get(Parameters.DIFF_UNLOCK_REQUEST):  # unset difflock
        #     if self._state == DriveState.NEUTRAL:
        #         self.diff_lock_request = 0
        #     self._data_store.set(Parameters.DIFF_UNLOCK_REQUEST, False)

        # if value := self._data_store.get(Parameters.JOYSTICK_MAPPING) != self.joystick_mapping:  # set joystickMapping
        #     if self._state == DriveState.NEUTRAL:
        #         if value in self._acceptable_joystick_maps:
        #             self.joystick_mapping = value

        # if value := self._data_store.get(Parameters.ACCELERATION) != self.acceleration:  # set Acceleration
        #     if self._state == DriveState.NEUTRAL:
        #         if self._acceleration_min <= value <= self._acceleration_max:
        #             self.acceleration = value

        # if value := self._data_store.get(Parameters.DECELERATION) != self.deceleration:  # set Deceleration
        #     if self._state == DriveState.NEUTRAL:
        #         if self._acceleration_min <= value <= self._acceleration_max:
        #             self.deceleration = value

        # if override := self._data_store.get(Parameters.INTERLOCK_OVERRIDE) != self.interlock_override:  # interlock override
        #     if override:
        #         self.interlock_override = 1
        #     else:
        #         self.interlock_override = 0

        # if self._data_store.get(Parameters.POWER_DOWN):  # power down
        #     if self._state == DriveState.NEUTRAL:
        #         if self._gpio.read(Pin.ACCESSORY_POWER) == 0:
        #             self._gpio.set(Pin.ACCESSORY_POWER, 1)

    def set_values(self):
        self._data_store.set(Parameters.SPEED, self.throttle)

    def transition(self, inputs: dict):
        # if inputs["seat"] == 0:  # TODO: add other interlocks
        #     if self._state != DriveState.NEUTRAL:
        #         print("DRIVE: transitioning to NEUTRAL (interlock triggered)")
        #
        # else:
        if inputs["forwards"] == 0 and inputs["reverse"] == 0:
            if self._state != DriveState.NEUTRAL:
                print("DRIVE: transitioning to NEUTRAL")
                self._state = DriveState.NEUTRAL
        elif inputs["forwards"] == 0 and inputs["reverse"] == 1:
            if self._state != DriveState.REVERSE:
                print("DRIVE: transitioning to REVERSE")
                self._state = DriveState.REVERSE
        elif inputs["forwards"] == 1 and inputs["reverse"] == 0:
            if self._state != DriveState.FORWARD:
                print("DRIVE: transitioning to FORWARD")
                self._state = DriveState.FORWARD

    def pulse_count(self):
        if time.perf_counter() - self._last_runtime_diff > self._diff_min_time:
            diff_pulse_count = binary_to_decimal(self._xpndr.read_gpio(3, "B"))
            self.diff_speed = diff_pulse_count / float(time.perf_counter() - self._last_runtime_diff) * 3600 / 54. * 25 * math.pi / 63360.  # [mph]
            self._xpndr.write_gpio(3, "A", [1, 1, 1, 1, 1, 1, 1, 1])
            self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 0, 0])
            self._last_runtime_diff = time.perf_counter()

    @staticmethod
    def calc_throttle(ground_speed_lever: float):
        return ground_speed_lever / 2800.0  # ((joystick - 584)/2802.)**4

    def step(self):
        self.update_values()

        gpio1a_values = self._xpndr.read_gpio(1, "A")
        gpio4a_values = self._xpndr.read_gpio(4, "A")
        ground_speed_lever = self._adc.read(1)

        inputs = {
            "brake_1": gpio1a_values[0],
            "brake_2": gpio1a_values[1],
            "seat": gpio1a_values[2],
            "diff_lock": gpio1a_values[3],
            "reverse": gpio4a_values[0],
            "forwards": gpio4a_values[1],
            "gsl": ground_speed_lever,
        }

        if self._state == DriveState.NEUTRAL or self._state == DriveState.PARK:
            self.clutch = 0
            self.brake = 0
            self.pump = 0
            self.fan = 0

            self.enable_motor = 0
            self.inching = 0

            self.neutral = 1
            self.forward = 0
            self.reverse = 0

            self.throttle = 0.0

        if self._state == DriveState.FORWARD and self.mode_pulling == 1:
            self.clutch = 1
            self.brake = 1
            self.pump = 1
            self.fan = 1

            self.inching = 0

            self.neutral = 0
            self.forward = 1
            self.reverse = 0

            if ground_speed_lever >= 843:
                self.throttle = self.calc_throttle(ground_speed_lever)
                self.enable_motor = 1
            else:
                self.throttle = 0.0
                self.enable_motor = 0

        if self._state == DriveState.FORWARD and self.mode_maneuverability == 1:
            self.clutch = 0
            self.brake = 1
            self.pump = 0
            self.fan = 0
            # self.fan = 1  # old

            self.neutral = 0
            self.forward = 1
            self.reverse = 0

            if ground_speed_lever >= 548:
                self.throttle = self.calc_throttle(ground_speed_lever)
                self.enable_motor = 1
            else:
                self.throttle = 0.0
                self.enable_motor = 0

        if self._state == DriveState.REVERSE:
            self.clutch = 0
            self.brake = 1
            self.pump = 0
            self.fan = 0
            # self.fan = 1  # old

            self.neutral = 0
            self.forward = 0
            self.reverse = 1

            self.inching = 0

            if ground_speed_lever >= 695:
                self.enable_motor = 1
            else:
                self.enable_motor = 0

            if ground_speed_lever >= 843:
                self.throttle = self.calc_throttle(ground_speed_lever)
                # self.throttle = ((ground_speed_lever - 843) / 2507.0) ** 2
            else:
                self.throttle = 0.0

        # calc pulse count for motor (for ground speed...?)
        self.pulse_count()

        # set outputs
        # self._xpndr.write_gpio(1, "B", [self.brake, self.clutch, 0, 0, 0, 0, self.pump, self.fan])
        # self._xpndr.write_gpio(4, "B", [0, self.inching, 0, self.reverse, self.forward, self.enable_motor, 0, 0])
        # self._xpndr.write_gpio(4, "B", [self.inching, 0, 0, 0, self.enable_motor, 0, self.reverse, self.forward])  # bad maybe...
        self._xpndr.write_gpio(1, "B", [self.fan, self.pump, 0, self.la_extend, self.la_retract, 0, self.clutch, self.brake])
        self._xpndr.write_gpio(3, "B", [0, self.inching, 0, self.reverse, self.forward, self.enable_motor, 0, 0])
        self._pot.set(self.throttle)

        # set values
        self.set_values()

        # transition to new state
        self.transition(inputs)

    def run(self):
        if time.perf_counter() >= self._last_runtime + DRIVE_STEP_INTERVAL:
            self.step()
            # self.test_step()  # TODO: switch back to main step
            self._last_runtime = time.perf_counter()

    def test_step(self):
        print("Testing...")

        # print("GPIO1: A-side input, B-side output, (blink & read)")
        # self._xpndr.write_gpio(1, "B", [1, 1, 1, 1, 1, 1, 1, 1])
        # self._xpndr.read_gpio(1, "A")
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "B", [0, 0, 0, 0, 0, 0, 0, 0])
        # self._xpndr.read_gpio(1, "A")
        # time.sleep(1)
        #
        # print("GPIO2: A-side input, B-side input, (read)")
        # self._xpndr.read_gpio(2, "A")
        # self._xpndr.read_gpio(2, "B")
        # time.sleep(1)
        #
        # print("GPIO3: A-side output, B-side input, (blink & read)")
        # self._xpndr.write_gpio(3, "A", [1, 1, 1, 1, 1, 1, 1, 1])
        # self._xpndr.read_gpio(3, "B")
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        # self._xpndr.read_gpio(3, "B")
        # time.sleep(1)
        #
        # print("GPIO4: A-side [I, I, O, O, O, O, O, O], B-side input, (blink & read)")
        # self._xpndr.write_gpio(1, "A", [1, 1, 0, 0, 0, 0, 0, 0])
        # self._xpndr.read_gpio(1, "A")
        # self._xpndr.read_gpio(1, "B")
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        # self._xpndr.read_gpio(1, "A")
        # self._xpndr.read_gpio(1, "B")
        # time.sleep(1)
        #
        # print("POT: 0.0 to 1.0 (increase)")
        # self._pot.set(0.0)
        # time.sleep(1)
        # self._pot.set(0.2)
        # time.sleep(1)
        # self._pot.set(0.4)
        # time.sleep(1)
        # self._pot.set(0.6)
        # time.sleep(1)
        # self._pot.set(0.8)
        # time.sleep(1)
        # self._pot.set(1.0)
        # time.sleep(1)
        #
        # print("ADC: reading channel 1")
        # self._adc.read(1)
        # time.sleep(1)

        # GPIO 1 (A) [ FAN_SIG, PUMP_SIG, _,    LA+SIG,    LA-SIG, INTERLOCK_OVERRIDE, CLUTCH_SIG,   BRAKE_SIG ]
        # GPIO 1 (B) [ BRAKE1,  BRAKE2,   SEAT, DIFF_LOCK, _,      _,                  OIL_PRESSURE, OIL_TEMP  ]

        # GPIO 2 (A) [ counter1 ... ]
        # GPIO 2 (B) [ counter2 ... ]

        # GPIO 3 (A) [ DIG_IN1_SIG, DIG_IN2_SIG, DIG_IN3_SIG, DIG_IN4_SIG, DIG_IN5_SIG, DIG_IN6_SIG, DIG_IN7_SIG, _ ]
        # GPIO 3 (B) [ NONE ]

        # GPIO 4 (A) [ FORWARDS, REVERSE, _,      RUNL_SIG, LHL_SIG,   RHL_SIG, RTL_SIG,     LTL_SIG     ]
        # GPIO 4 (B) [ R_TURN,   L_TURN,  HAZARD, LIGHTS,   RUN_LIGHT, _,       COUNTER1_RS, COUNTER2_RS ]
        #              FORWARD,  REVERSE

        self._xpndr.write_gpio(3, "B", [1, 0, 0, 0, 0, 0, 0, 0])  # D_IN1
        time.sleep(1)
        self._xpndr.write_gpio(3, "B", [0, 1, 0, 0, 0, 0, 0, 0])  # D_IN2
        time.sleep(1)
        self._xpndr.write_gpio(3, "B", [0, 0, 1, 0, 0, 0, 0, 0])  # D_IN3
        time.sleep(1)
        self._xpndr.write_gpio(3, "B", [0, 0, 0, 1, 0, 0, 0, 0])  # D_IN4
        time.sleep(1)
        self._xpndr.write_gpio(3, "B", [0, 0, 0, 0, 1, 0, 0, 0])  # D_IN5
        time.sleep(1)
        self._xpndr.write_gpio(3, "B", [0, 0, 0, 0, 0, 1, 0, 0])  # D_IN6
        time.sleep(1)
        self._xpndr.write_gpio(3, "B", [0, 0, 0, 0, 0, 0, 1, 0])  # D_IN7
        time.sleep(1)
        self._xpndr.write_gpio(1, "B", [1, 0, 0, 0, 0, 0, 0, 0])  # FAN
        time.sleep(1)
        self._xpndr.write_gpio(1, "B", [0, 1, 0, 0, 0, 0, 0, 0])  # PUMP
        time.sleep(1)
        self._xpndr.write_gpio(1, "B", [0, 0, 0, 0, 0, 0, 1, 0])  # CLUTCH
        time.sleep(1)
        self._xpndr.write_gpio(1, "B", [0, 0, 0, 0, 0, 0, 0, 1])  # BRAKE
        time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 1, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 1, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 0, 1, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 0, 0, 1, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 0, 0, 0, 1])
        # time.sleep(1)
        # self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        #
        # self._xpndr.write_gpio(3, "A", [1, 0, 0, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 1, 0, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 1, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 1, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 1, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 1, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 1, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 0, 1])
        # time.sleep(1)
        # self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        #
        # self._xpndr.write_gpio(4, "A", [1, 0, 0, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 1, 0, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 0, 0, 1, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 0, 0, 0, 1, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 0, 0, 0, 0, 1, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 0, 0, 0, 0, 0, 1, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 0, 0, 0, 0, 0, 0, 1])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        #
        # self._xpndr.write_gpio(4, "B", [1, 0, 0, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "B", [0, 1, 0, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "B", [0, 0, 1, 0, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "B", [0, 0, 0, 1, 0, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "B", [0, 0, 0, 0, 1, 0, 0, 0])
        # time.sleep(1)
        # self._xpndr.write_gpio(4, "B", [0, 0, 0, 0, 0, 0, 0, 0])


DRIVE_STEP_INTERVAL = 1
