import math
import time

from controller import GpioHandler, Expander, Potentiometer, AnalogDigitalConverter, RpiPin as Pin, binary_to_decimal
from database import DataStore, Parameters

# TODO: create functions for state machine logic, break up into 'states'/'transitions'
# TODO: replace time.time() with time.perf_counter() for accuracy
# TODO: further abstraction, drive_state_machine.py should be purely logic, no reference to specific GPIO pins


class DriveStateMachine:
    accPwr = 1

    bounceTimeThreshN = 1
    bounceTimeThresh = 1

    motorEnableSuccess = 0

    acceptableJoystickMaps = [0]
    accelMax = 1
    accelMin = 1
    diffMinTime = 0.5

    def __init__(self):
        self._gpio = GpioHandler()
        self._xpndr = Expander()
        self._pot = Potentiometer()
        self._adc = AnalogDigitalConverter()

        # internally calculated
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
        self.modeManeuverability = 1
        self.modePulling = 0
        self.diffLockRequest = 0
        self.joystickMapping = 0  # 0 = linear
        self.Acceleration = 0  # 0 = no limitation
        self.Deceleration = 0  # 0 = no limitation
        self.interlockOverride = 0

        self.diffLastTime = time.perf_counter()
        self._last_runtime = time.perf_counter()

    def initialize(self):
        self._gpio.init_output(Pin.POWER_DOWN)
        self._gpio.init_input(Pin.ACCESSORY_POWER)

        self._gpio.set(Pin.POWER_DOWN, 0)

    def step(self):
        gpio1a_values = self._xpndr.read_gpio(1, "A")
        joystick = self._adc.read(1)
        if self.neutral == 1:
            inching = 0
            self.brake = 0
            self.clutch = 0
            self.enable_motor = 0
            self.throttle = 0.0
            self.fans = 0

            if gpio1a_values[3] == 1 and gpio1a_values[2] == 0 and (1 not in self.gear_lockout) and self.bounce_timer != 0 and time.perf_counter() > self.bounce_timer + self.bounceTimeThreshN:
                if joystick <= 548:
                    self.forwards = 1
                    self.reverse = 0
                    self.neutral = 0
                else:
                    gear_lockout_001 = 1
            elif gpio1a_values[2] == 1 and gpio1a_values[3] == 0 and (1 not in self.gear_lockout) and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounceTimeThreshN:
                if joystick <= 548:
                    self.forwards = 0
                    self.reverse = 1
                    self.neutral = 0
                else:
                    print('Pull Joystick back to switch to Reverse')
                    gear_lockout_001 = 1

            if joystick <= 548 and gpio1a_values[2] == 0 and gpio1a_values[3] == 0:
                self.gear_lockout[0] = 0
                self.gear_lockout[1] = 0

            if (gpio1a_values[3] == 1 or gpio1a_values[2] == 1) and self.bounce_timer == 0:
                self.bounce_timer = time.time()

            if self.bounce_timer != 0 and (gpio1a_values[3] == 0 and gpio1a_values[2] == 0):
                self.bounce_timer = 0

        if self.forwards == 1 and self.modePulling == 1:
            self.fans = 1
            inching = 0

            if joystick <= 548:
                self.brake = 1
            else:
                brake = 0
            if joystick >= 695:
                self.clutch = 1
            else:
                self.clutch = 0
            if joystick >= 843:
                self.throttle = (joystick - 843) / 2507.
                self.enable_motor = 1
            else:
                self.throttle = 0.
                self.enable_motor = 0

            if gpio1a_values[3] == 0 and self.bounce_timer != 0 and time.perf_counter() > self.bounce_timer + self.bounceTimeThresh:
                self.forwards = 0
                self.reverse = 0
                self.neutral = 1
                self.enable_motor = 0
                self.throttle = 0.
                self.brake = 0
                self.clutch = 0
                self.fans = 0

            if gpio1a_values[3] == 0 and self.bounce_timer == 0:
                self.bounce_timer = time.time()

            if self.bounce_timer != 0 and gpio1a_values[3] == 1:
                self.bounce_timer = 0

        if self.forwards == 1 and self.modeManeuverability == 1:
            self.fans = 1
            self.brake = 1
            self.clutch = 0

            if joystick >= 548:
                self.throttle = ((joystick - 584) / 2802.)  # ((joystick - 584)/2802.)**4
                self.enable_motor = 1
            else:
                self.throttle = 0.
                self.enable_motor = 0
            # if 548 <= joystick <= 695:
            #    inching = 1
            # else:
            #    inching = 0

            if gpio1a_values[3] == 0 and self.bounce_timer != 0 and time.perf_counter() > self.bounce_timer + self.bounceTimeThresh:
                self.forwards = 0
                self.reverse = 0
                self.neutral = 1
                self.enable_motor = 0
                self.throttle = 0.
                self.brake = 0
                self.clutch = 0
                self.fans = 0

            if gpio1a_values[3] == 0 and self.bounce_timer == 0:
                self.bounce_timer = time.perf_counter()

            if self.bounce_timer != 0 and gpio1a_values[3] == 1:
                self.bounce_timer = 0

        if self.reverse == 1:
            self.brake = 1
            self.clutch = 0
            self.fans = 1
            inching = 0

            if joystick >= 695:
                self.enable_motor = 1
            else:
                self.enable_motor = 0
            if joystick >= 843:
                self.throttle = ((joystick - 843) / 2507.) ** 2
            else:
                self.throttle = 0.

            if gpio1a_values[2] == 0 and self.bounce_timer != 0 and time.time() > self.bounce_timer + self.bounceTimeThresh:
                self.forwards = 0
                self.reverse = 0
                self.neutral = 1
                self.enable_motor = 0
                self.throttle = 0.
                self.brake = 0
                self.clutch = 0
                self.fans = 0

            if gpio1a_values[2] == 0 and self.bounce_timer == 0:
                self.bounce_timer = time.perf_counter()

            if self.bounce_timer != 0 and gpio1a_values[2] == 1:
                self.bounce_timer = 0

        if time.time() - self.diffLastTime > self.diffMinTime:
            diffPulseCount = binaryToDecimal(readGPIOB(p_GPIO3Select))
            self.diff_speed = diffPulseCount / float(time.time() - self.diffLastTime) * 3600 / 54. * 25 * math.pi / 63360.  # [mph]
            writeGPIOA(p_GPIO3Select, [1, 1, 1, 1, 1, 1, 1, 1])
            writeGPIOA(p_GPIO3Select, [0, 0, 0, 0, 0, 0, 0, 0])
            diffLastTime = time.time()

        writeGPIOB(p_GPIO1Select, [self.brake, self.clutch, 0, 0, 0, 0, self.fans, self.fans])
        writeGPIOB(p_GPIO4Select, [0, inching, 0, self.reverse, self.forwards, self.enable_motor, 0, 0])

        setPot(self.throttle)

        Quido.put((brake, clutch, throttle, enableMotor, forwards, reverse,
                   neutral, gearlockout, fans, pump, LAExtend, LARetract,
                   gpio1a_values, modeManeuverability, modePulling, diffSpeed,
                   accPwr))
        try:
            data = Quodi.get(False)
        except:
            data = None

        if data:
            if data[0] == 1:  # set to maneuverability
                if self.neutral == 1:
                    self.modeManeuverability = 1
                    self.modePulling = 0
            if data[0] == 2:  # set to pulling
                if self.neutral == 1:
                    self.modeManeuverability = 0
                    self.modePulling = 1
            if data[0] == 3:  # set/unset difflock
                if self.neutral == 1:
                    if data[1] == 1:
                        diffLockRequest = 1
                    elif data[1] == 0:
                        diffLockRequest = 0
            if data[0] == 4:  # set joystickMapping
                if neutral == 1:
                    if data[1] in acceptableJoystickMaps:
                        joystickMapping = data[1]
            if data[0] == 5:  # set Acceleration
                if neutral == 1:
                    if accelMin <= data[1] <= accelMax:
                        Acceleration = data[1]
            if data[0] == 6:  # set Acceleration
                if neutral == 1:
                    if accelMin <= data[1] <= accelMax:
                        Deceleration = data[1]
            if data[0] == 7:  # interlock override
                if data[1] == 1:
                    interlockOverride = 1
                elif data[1] == 0:
                    interlockOverride = 0

            if data[0] == 100:  # powerdown
                if neutral == 1:
                    if GPIO.input(p_AccessoryPower) == 0:
                        # GPIO.output(p_powerDown, 1)
                        pass

    def run(self):
        if time.perf_counter() >= self._last_runtime + DRIVE_STEP_INTERVAL:
            self.test_step()  # TODO: switch back to main step
            self._last_runtime = time.perf_counter()

    def test_step(self):
        print("Testing...")

        print("GPIO1: A-side input, B-side output, (blink & read)")
        self._xpndr.write_gpio(1, "B", [1, 1, 1, 1, 1, 1, 1, 1])
        self._xpndr.read_gpio(1, "A")
        time.sleep(1)
        self._xpndr.write_gpio(1, "B", [0, 0, 0, 0, 0, 0, 0, 0])
        self._xpndr.read_gpio(1, "A")
        time.sleep(1)

        print("GPIO2: A-side input, B-side input, (read)")
        self._xpndr.read_gpio(2, "A")
        self._xpndr.read_gpio(2, "B")
        time.sleep(1)

        print("GPIO3: A-side output, B-side input, (blink & read)")
        self._xpndr.write_gpio(3, "A", [1, 1, 1, 1, 1, 1, 1, 1])
        self._xpndr.read_gpio(3, "B")
        time.sleep(1)
        self._xpndr.write_gpio(3, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        self._xpndr.read_gpio(3, "B")
        time.sleep(1)

        print("GPIO4: A-side [I, I, O, O, O, O, O, O], B-side input, (blink & read)")
        self._xpndr.write_gpio(1, "A", [1, 1, 0, 0, 0, 0, 0, 0])
        self._xpndr.read_gpio(1, "A")
        self._xpndr.read_gpio(1, "B")
        time.sleep(1)
        self._xpndr.write_gpio(1, "A", [0, 0, 0, 0, 0, 0, 0, 0])
        self._xpndr.read_gpio(1, "A")
        self._xpndr.read_gpio(1, "B")
        time.sleep(1)

        print("POT: 0.0 to 1.0 (increase)")
        self._pot.set(0.0)
        time.sleep(1)
        self._pot.set(0.2)
        time.sleep(1)
        self._pot.set(0.4)
        time.sleep(1)
        self._pot.set(0.6)
        time.sleep(1)
        self._pot.set(0.8)
        time.sleep(1)
        self._pot.set(1.0)
        time.sleep(1)

        print("ADC: reading channel 1")
        self._adc.read(1)
        time.sleep(1)

# def run(Quodi, Quido):
#     initGPIO()
#     initXPNDR()
#     initPot()
#
#     writeGPIOA(p_GPIO3Select, [1, 1, 1, 1, 1, 1, 1, 1])
#     writeGPIOA(p_GPIO3Select, [0, 0, 0, 0, 0, 0, 0, 0])


DRIVE_STEP_INTERVAL = 1
