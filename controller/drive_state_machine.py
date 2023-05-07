# import math
# import time
#
# from controller import GPIOHandler
# from database import DataStore, LiveData as lD, StoredData as sD
# from common import binary_to_decimal
#
# # TODO: create functions for state machine logic, break up into 'states'/'transitions'
# # TODO: replace time.time() with time.perf_counter() for accuracy
# # TODO: further abstraction, drive_state_machine.py should be purely logic, no reference to specific GPIO pins
#
#
# class DriveStateMachine:
#     def __init__(self):
#         # external class
#         self.data_store = DataStore()
#         self.gpio = GPIOHandler()
#
#         # timer values
#         self.last_run = time.perf_counter()
#         self.diff_last_time = time.perf_counter()
#
#         # data values
#         self.external = {}
#         self.internal = {}
#         self.constants = {}
#
#         # initialize data values
#         self.update_values(Values.ALL)
#
#         # constant values
#         self.acc_pwr = 1
#         self.bounce_time_thresh_n = 1
#         self.bounce_time_thresh = 1
#         self.motor_enable_success = 0
#         self.acceptable_joystick_maps = [0]
#         self.accel_max = 1
#         self.accel_min = 1
#         self.diff_min_time = 0.5
#
#         # internally calculated
#         self.inching = 0
#         self.brake = 0
#         self.clutch = 0
#         self.throttle = 0
#         self.enable_motor = 0
#         self.forwards = 0
#         self.reverse = 0
#         self.neutral = 1
#         self.gear_lockout = [0, 0]
#         self.fans = 0
#         self.pump = 0
#         self.la_extend = 0
#         self.la_retract = 0
#         self.bounce_timer = 0
#         self.diff_speed = 0
#
#         # externally set
#         self.mode_maneuverability = 1
#         self.mode_pulling = 0
#         self.diff_lock_request = 0
#         self.joystick_mapping = 0  # 0 = linear
#         self.acceleration = 0  # 0 = no limitation
#         self.deceleration = 0  # 0 = no limitation
#         self.interlock_override = 0
#
#         self.test = self.data_store.get(lD.TEST_PARAM)
#
#         self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [1, 1, 1, 1, 1, 1, 1, 1], "A")  # TODO: should be further abstracted
#         self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [0, 0, 0, 0, 0, 0, 0, 0], "A")
#
#     def update_values(self):
#         """
#         Update the data values for the State Machine. Categories for values are determined by enum `Values`.
#         """
#
#         # if values == Values.INTERNAL or values == Values.ALL:
#         #     self.internal = self.data_store.get_many([
#         #         lD.INCHING,
#         #         lD.BRAKE,
#         #         lD.CLUTCH,
#         #         lD.THROTTLE,
#         #         lD.ENABLE_MOTOR,
#         #         lD.FORWARDS,
#         #         lD.REVERSE,
#         #         lD.NEUTRAL,
#         #         lD.GEAR_LOCKOUT,
#         #         lD.FANS,
#         #         lD.PUMP,
#         #         lD.LA_EXTEND,
#         #         lD.LA_RETRACT,
#         #         lD.BOUNCE_TIMER,
#         #         lD.DIFF_SPEED,
#         #     ])
#
#         # external = self.data_store.get_many([
#         #     lD.MODE_MANEUVERABILITY,
#         #     lD.MODE_PULLING,
#         #     lD.DIFF_LOCK_REQUEST,
#         #     lD.JOYSTICK_MAPPING,
#         #     lD.ACCELERATION,
#         #     lD.DECELERATION,
#         #     lD.INTERLOCK_OVERRIDE,
#         # ])
#         #
#         # self.mode_maneuverability = external[lD.MODE_MANEUVERABILITY.name]
#         # self.mode_pulling = external[lD.MODE_PULLING.name]
#         # self.diff_lock_request = external[lD.DIFF_LOCK_REQUEST.name]
#         # self.joystick_mapping = external[lD.JOYSTICK_MAPPING.name]
#         # self.acceleration = external[lD.ACCELERATION.name]
#         # self.deceleration = external[lD.DECELERATION.name]
#         # self.interlock_override = external[lD.INTERLOCK_OVERRIDE.name]
#
#         # if values == Values.CONSTANTS or values == Values.ALL:
#         #     self.constants = self.data_store.get_many([
#         #         sD.ACC_POWER,
#         #         sD.BOUNCE_TIME_THRESHOLD_N,
#         #         sD.BOUNCE_TIME_THRESHOLD,
#         #         sD.MOTOR_ENABLE_SUCCESS,
#         #         sD.ACCEPTABLE_JOYSTICK_MAPS,
#         #         sD.ACCELERATION_MAX,
#         #         sD.ACCELERATION_MIN,
#         #         sD.DIFF_MIN_TIME,
#         #     ])
#
#     def update_external_values(self):
#         external = self.data_store.get_many([
#             lD.MODE_MANEUVERABILITY,
#             lD.MODE_PULLING,
#             lD.DIFF_LOCK_REQUEST,
#             lD.JOYSTICK_MAPPING,
#             lD.ACCELERATION,
#             lD.DECELERATION,
#             lD.INTERLOCK_OVERRIDE,
#         ])
#         self.mode_maneuverability = external[lD.MODE_MANEUVERABILITY.name]
#         self.mode_pulling = external[lD.MODE_PULLING.name]
#         self.diff_lock_request = external[lD.DIFF_LOCK_REQUEST.name]
#         self.joystick_mapping = external[lD.JOYSTICK_MAPPING.name]
#         self.acceleration = external[lD.ACCELERATION.name]
#         self.deceleration = external[lD.DECELERATION.name]
#         self.interlock_override = external[lD.INTERLOCK_OVERRIDE.name]
#
#     def update_internal_values(self):
#         self.internal = self.data_store.set_many({
#             lD.INCHING: self.inching,
#             lD.BRAKE: self.brake,
#             lD.CLUTCH: self.clutch,
#             lD.THROTTLE: self.throttle,
#             lD.ENABLE_MOTOR: self.enable_motor,
#             lD.FORWARDS: self.forwards,
#             lD.REVERSE: self.reverse,
#             lD.NEUTRAL: self.neutral,
#             lD.GEAR_LOCKOUT: self.gear_lockout,
#             lD.FANS: self.fans,
#             lD.PUMP: self.pump,
#             lD.LA_EXTEND: self.la_extend,
#             lD.LA_RETRACT: self.la_retract,
#             lD.BOUNCE_TIMER: self.bounce_timer,
#             lD.DIFF_SPEED: self.diff_speed,
#         })
#
#     def set_values(self, values: Values):
#         """
#         Set the current data values to the Redis Data Store. Categories for values are determined by enum `Values`.
#
#         NOTE: Care should be taken as to when this function is called to ensure externally updated values are not
#         accidentally overwritten.
#         """
#
#         pass
#
#     def step(self):
#         gpio_values_1a = self.gpio.read_gpio(GpioPin.GPIO1_SELECT, "A")
#         joystick_value = self.gpio.read_adc(1)
#         if self.neutral == 1:
#             self.inching = 0
#             self.brake = 0
#             self.clutch = 0
#             self.enable_motor = 0
#             self.throttle = 0.
#             self.fans = 0
#
#             if gpio_values_1a[3] == 1 and gpio_values_1a[2] == 0 and (1 not in self.gear_lockout) and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh_n:
#                 if joystick_value <= 548:
#                     self.forwards = 1
#                     self.reverse = 0
#                     self.neutral = 0
#                 else:
#                     self.gear_lockout_001 = 1
#             elif gpio_values_1a[2] == 1 and gpio_values_1a[3] == 0 and (1 not in self.gear_lockout) and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh_n:
#                 if joystick_value <= 548:
#                     self.forwards = 0
#                     self.reverse = 1
#                     self.neutral = 0
#                 else:
#                     print('Pull Joystick back to switch to Reverse')
#                     self.gear_lockout_001 = 1
#
#             if joystick_value <= 548 and gpio_values_1a[2] == 0 and gpio_values_1a[3] == 0:
#                 self.gear_lockout[0] = 0
#                 self.gear_lockout[1] = 0
#
#             if (gpio_values_1a[3] == 1 or gpio_values_1a[2] == 1) and self.bounce_timer == 0:
#                 self.bounce_timer = time.time()
#
#             if self.bounce_timer != 0 and (gpio_values_1a[3] == 0 and gpio_values_1a[2] == 0):
#                 self.bounce_timer = 0
#
#         if self.forwards == 1 and self.mode_pulling == 1:
#             self.fans = 1
#             self.inching = 0
#
#             if joystick_value <= 548:
#                 self.brake = 1
#             else:
#                 self.brake = 0
#
#             if joystick_value >= 695:
#                 self.clutch = 1
#             else:
#                 self.clutch = 0
#
#             if joystick_value >= 843:
#                 self.throttle = (joystick_value - 843) / 2507.
#                 self.enable_motor = 1
#             else:
#                 self.throttle = 0.
#                 self.enable_motor = 0
#
#             if gpio_values_1a[3] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh:
#                 self.forwards = 0
#                 self.reverse = 0
#                 self.neutral = 1
#                 self.enable_motor = 0
#                 self.throttle = 0.
#                 self.brake = 0
#                 self.clutch = 0
#                 self.fans = 0
#
#             if gpio_values_1a[3] == 0 and self.bounce_timer == 0:
#                 self.bounce_timer = time.time()
#
#             if self.bounce_timer != 0 and gpio_values_1a[3] == 1:
#                 self.bounce_timer = 0
#
#         if self.forwards == 1 and self.mode_maneuverability == 1:
#             self.fans = 1
#             self.brake = 1
#             self.clutch = 0
#
#             if joystick_value >= 548:
#                 self.throttle = ((joystick_value - 584) / 2802.)  # ((joystick - 584)/2802.)**4
#                 self.enable_motor = 1
#             else:
#                 self.throttle = 0.
#                 self.enable_motor = 0
#
#             if gpio_values_1a[3] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh:
#                 self.forwards = 0
#                 self.reverse = 0
#                 self.neutral = 1
#                 self.enable_motor = 0
#                 self.throttle = 0.
#                 self.brake = 0
#                 self.clutch = 0
#                 self.fans = 0
#
#             if gpio_values_1a[3] == 0 and self.bounce_timer == 0:
#                 self.bounce_timer = time.time()
#
#             if self.bounce_timer != 0 and gpio_values_1a[3] == 1:
#                 self.bounce_timer = 0
#
#         if self.reverse == 1:
#             self.brake = 1
#             self.clutch = 0
#             self.fans = 1
#             self.inching = 0
#
#             if joystick_value >= 695:
#                 self.enable_motor = 1
#             else:
#                 self.enable_motor = 0
#             if joystick_value >= 843:
#                 self.throttle = ((joystick_value - 843) / 2507.) ** 2
#             else:
#                 throttle = 0.
#
#             if gpio_values_1a[
#                 2] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounce_time_thresh:
#                 self.forwards = 0
#                 self.reverse = 0
#                 self.neutral = 1
#                 self.enable_motor = 0
#                 self.throttle = 0.
#                 self.brake = 0
#                 self.clutch = 0
#                 self.fans = 0
#
#             if gpio_values_1a[2] == 0 and self.bounce_timer == 0:
#                 self.bounce_timer = time.time()
#
#             if self.bounce_timer != 0 and gpio_values_1a[2] == 1:
#                 self.bounce_timer = 0
#
#         if time.time() - self.diff_last_time > self.diff_min_time:
#             diff_pulse_count = binary_to_decimal(self.gpio.read_gpio(GpioPin.GPIO3_SELECT, "B"))
#             self.diff_speed = diff_pulse_count / float(
#                 time.time() - self.diff_last_time) * 3600 / 54. * 25 * math.pi / 63360.  # [mph]
#             self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [1, 1, 1, 1, 1, 1, 1, 1], "A")
#             self.gpio.write_gpio(GpioPin.GPIO3_SELECT, [0, 0, 0, 0, 0, 0, 0, 0], "A")
#             self.diff_last_time = time.time()
#
#         self.gpio.write_gpio(GpioPin.GPIO1_SELECT, [self.brake, self.clutch, 0, 0, 0, 0, self.fans, self.fans], "B")
#         self.gpio.write_gpio(GpioPin.GPIO4_SELECT,
#                              [0, self.inching, 0, self.reverse, self.forwards, self.enable_motor, 0, 0], "B")
#
#         self.gpio.set_pot(self.throttle)
#
#         # TODO: set and get values from data_store
#         # Quido.put((brake, clutch, throttle, enableMotor, forwards, reverse,
#         #            neutral, gearlockout, fans, pump, LAExtend, LARetract,
#         #            GPIO1AValues, modeManeuverability, modePulling, diffSpeed,
#         #            accPwr))
#
#         self.update_internal_values()
#
#         # try:
#         #     data = Quodi.get(False)
#         # except:
#         #     data = None
#
#         self.update_external_values()
#
#         # if data[0] == 1:  # set to maneuverability
#         #     if self.neutral == 1:
#         #         self.mode_maneuverability = 1
#         #         self.mode_pulling = 0
#         # if data[0] == 2:  # set to pulling
#         #     if self.neutral == 1:
#         #         self.mode_maneuverability = 0
#         #         self.mode_pulling = 1
#         # if data[0] == 3:  # set/unset difflock
#         #     if self.neutral == 1:
#         #         if data[1] == 1:
#         #             self.diff_lock_request = 1
#         #         elif data[1] == 0:
#         #             self.diff_lock_request = 0
#         # if data[0] == 4:  # set joystickMapping
#         #     if self.neutral == 1:
#         #         if data[1] in self.acceptable_joystick_maps:
#         #             self.joystick_mapping = data[1]
#         # if data[0] == 5:  # set Acceleration
#         #     if self.neutral == 1:
#         #         if self.accel_min <= data[1] <= self.accel_max:
#         #             self.acceleration = data[1]
#         # if data[0] == 6:  # set Acceleration
#         #     if self.neutral == 1:
#         #         if self.accel_min <= data[1] <= self.accel_max:
#         #             self.deceleration = data[1]
#         # if data[0] == 7:  # interlock override
#         #     if data[1] == 1:
#         #         self.interlock_override = 1
#         #     elif data[1] == 0:
#         #         self.interlock_override = 0
#         #
#         # if data[0] == 100:  # powerdown
#         #     if self.neutral == 1:
#         #         if GPIO.input(p_AccessoryPower) == 0:
#         #             # GPIO.output(p_powerDown, 1)
#         #             pass
#
#     def run(self):
#         if self.last_run + STEP_INTERVAL < time.perf_counter():
#             self.last_run = time.perf_counter()
#             self.step()
#
#
# STEP_INTERVAL = 1
