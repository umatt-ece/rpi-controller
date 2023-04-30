import math
import time

from controller import GPIOHandler, GpioPin, binary_to_decimal
from database import DataStore, LiveData as lD


# TODO: create functions for state machine logic, break up into 'states'/'transitions'
# TODO: replace time.time() with time.perf_counter() for accuracy


class StateMachine:
    def __init__(self):
        self.data_store = DataStore()
        self.gpio = GPIOHandler()

        self.last_run = time.perf_counter()
        self.values = {}

        self.acc_pwr = 1
        self.bounce_time_thresh_n = 1
        self.bounce_time_thresh = 1
        self.motor_enable_success = 0
        self.acceptable_joystick_maps = [0]
        self.accel_max = 1
        self.accel_min = 1
        self.diff_min_time = 0.5

        # internally calculated
        self.inching = 0
        self.brake = 0
        self.clutch = 0
        self.throttle = 0
        self.enable_motor = 0
        self.forwards = 0
        self.reverse = 0
        self.neutral = 1
        self.gear_lockout = [0, 0]
        self.fans = 0
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

        self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [1, 1, 1, 1, 1, 1, 1, 1], "A")
        self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [0, 0, 0, 0, 0, 0, 0, 0], "A")

        self.diff_last_time = time.time()

    def update_values(self):
        self.values = self.data_store.get_many([
            lD.GEAR,  # TODO: fetch the values we want from redis for each step...
        ])

    def step(self):
        gpio_values_1a = self.gpio.read_gpio(GpioPin.GPIO1_SELECT, "A")
        joystick_value = self.gpio.read_adc(1)
        if self.neutral == 1:
            self.inching = 0
            self.brake = 0
            self.clutch = 0
            self.enable_motor = 0
            self.throttle = 0.
            self.fans = 0

            if gpio_values_1a[3] == 1 and gpio_values_1a[2] == 0 and (
                    1 not in self.gear_lockout) and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh_n:
                if joystick_value <= 548:
                    self.forwards = 1
                    self.reverse = 0
                    self.neutral = 0
                else:
                    self.gear_lockout_001 = 1
            elif gpio_values_1a[2] == 1 and gpio_values_1a[3] == 0 and (
                    1 not in self.gear_lockout) and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh_n:
                if joystick_value <= 548:
                    self.forwards = 0
                    self.reverse = 1
                    self.neutral = 0
                else:
                    print('Pull Joystick back to switch to Reverse')
                    self.gear_lockout_001 = 1

            if joystick_value <= 548 and gpio_values_1a[2] == 0 and gpio_values_1a[3] == 0:
                self.gear_lockout[0] = 0
                self.gear_lockout[1] = 0

            if (gpio_values_1a[3] == 1 or gpio_values_1a[2] == 1) and self.bounce_timer == 0:
                self.bounce_timer = time.time()

            if self.bounce_timer != 0 and (gpio_values_1a[3] == 0 and gpio_values_1a[2] == 0):
                self.bounce_timer = 0

        if self.forwards == 1 and self.mode_pulling == 1:
            self.fans = 1
            self.inching = 0

            if joystick_value <= 548:
                self.brake = 1
            else:
                self.brake = 0

            if joystick_value >= 695:
                self.clutch = 1
            else:
                self.clutch = 0

            if joystick_value >= 843:
                self.throttle = (joystick_value - 843) / 2507.
                self.enable_motor = 1
            else:
                self.throttle = 0.
                self.enable_motor = 0

            if gpio_values_1a[
                3] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh:
                self.forwards = 0
                self.reverse = 0
                self.neutral = 1
                self.enable_motor = 0
                self.throttle = 0.
                self.brake = 0
                self.clutch = 0
                self.fans = 0

            if gpio_values_1a[3] == 0 and self.bounce_timer == 0:
                self.bounce_timer = time.time()

            if self.bounce_timer != 0 and gpio_values_1a[3] == 1:
                self.bounce_timer = 0

        if self.forwards == 1 and self.mode_maneuverability == 1:
            self.fans = 1
            self.brake = 1
            self.clutch = 0

            if joystick_value >= 548:
                self.throttle = ((joystick_value - 584) / 2802.)  # ((joystick - 584)/2802.)**4
                self.enable_motor = 1
            else:
                self.throttle = 0.
                self.enable_motor = 0

            if gpio_values_1a[
                3] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh:
                self.forwards = 0
                self.reverse = 0
                self.neutral = 1
                self.enable_motor = 0
                self.throttle = 0.
                self.brake = 0
                self.clutch = 0
                self.fans = 0

            if gpio_values_1a[3] == 0 and self.bounce_timer == 0:
                self.bounce_timer = time.time()

            if self.bounce_timer != 0 and gpio_values_1a[3] == 1:
                self.bounce_timer = 0

        if self.reverse == 1:
            self.brake = 1
            self.clutch = 0
            self.fans = 1
            self.inching = 0

            if joystick_value >= 695:
                self.enable_motor = 1
            else:
                self.enable_motor = 0
            if joystick_value >= 843:
                self.throttle = ((joystick_value - 843) / 2507.) ** 2
            else:
                throttle = 0.

            if gpio_values_1a[
                2] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh:
                self.forwards = 0
                self.reverse = 0
                self.neutral = 1
                self.enable_motor = 0
                self.throttle = 0.
                self.brake = 0
                self.clutch = 0
                self.fans = 0

            if gpio_values_1a[2] == 0 and self.bounce_timer == 0:
                self.bounce_timer = time.time()

            if self.bounce_timer != 0 and gpio_values_1a[2] == 1:
                self.bounce_timer = 0

        if time.time() - self.diff_last_time > self.diff_min_time:
            diff_pulse_count = binary_to_decimal(self.gpio.read_gpio(GpioPin.GPIO3_SELECT, "B"))
            self.diff_speed = diff_pulse_count / float(
                time.time() - self.diff_last_time) * 3600 / 54. * 25 * math.pi / 63360.  # [mph]
            self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [1, 1, 1, 1, 1, 1, 1, 1], "A")
            self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [0, 0, 0, 0, 0, 0, 0, 0], "A")
            self.diff_last_time = time.time()

        self.gpio.write_gpio(GpioPin.GPIO1_SELECT, [self.brake, self.clutch, 0, 0, 0, 0, self.fans, self.fans], "B")
        self.gpio.write_gpio(GpioPin.GPIO4_SELECT,
                             [0, self.inching, 0, self.reverse, self.forwards, self.enable_motor, 0, 0], "B")

        self.gpio.set_pot(self.throttle)

        # TODO: set and get values from data_store
        # Quido.put((brake, clutch, throttle, enableMotor, forwards, reverse,
        #            neutral, gearlockout, fans, pump, LAExtend, LARetract,
        #            GPIO1AValues, modeManeuverability, modePulling, diffSpeed,
        #            accPwr))
        # try:
        #     data = Quodi.get(False)
        # except:
        #     data = None
        #
        # if data:
        #     if data[0] == 1:  # set to maneuverability
        #         if neutral == 1:
        #             modeManeuverability = 1
        #             modePulling = 0
        #     if data[0] == 2:  # set to pulling
        #         if neutral == 1:
        #             modeManeuverability = 0
        #             modePulling = 1
        #     if data[0] == 3:  # set/unset difflock
        #         if neutral == 1:
        #             if data[1] == 1:
        #                 diffLockRequest = 1
        #             elif data[1] == 0:
        #                 diffLockRequest = 0
        #     if data[0] == 4:  # set joystickMapping
        #         if neutral == 1:
        #             if data[1] in acceptableJoystickMaps:
        #                 joystickMapping = data[1]
        #     if data[0] == 5:  # set Acceleration
        #         if neutral == 1:
        #             if accelMin <= data[1] <= accelMax:
        #                 Acceleration = data[1]
        #     if data[0] == 6:  # set Acceleration
        #         if neutral == 1:
        #             if accelMin <= data[1] <= accelMax:
        #                 Deceleration = data[1]
        #     if data[0] == 7:  # interlock override
        #         if data[1] == 1:
        #             interlockOverride = 1
        #         elif data[1] == 0:
        #             interlockOverride = 0
        #
        #     if data[0] == 100:  # powerdown
        #         if neutral == 1:
        #             if GPIO.input(p_AccessoryPower) == 0:
        #                 # GPIO.output(p_powerDown, 1)
        #                 pass

    def run(self):
        if self.last_run + STEP_INTERVAL < time.perf_counter():
            self.last_run = time.perf_counter()
            self.step()


STEP_INTERVAL = 1
