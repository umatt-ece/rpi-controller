from enum import Enum

from controller import int_to_binary, binary_to_decimal
from database import DataStore, LiveData as lD
from common import RpiPin as Pin


# TODO: the old controller used this library
import RPi.GPIO as GPIO
# TODO: this library supports SPI, maybe also consider pigpio which supports SPI, I2C, and UART
# import gpiozero as gpio


class GPIOHandler:
    def __init__(self):
        print("Initializing GPIO Handler...")
        self.data_store = DataStore()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def init_input(self, pin: pin):

    def init_pot(self):
        value = 1.0
        message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        self.write_spi(pin.POT_SELECT.value, message)

    def init_xpndr(self):
        self.write_spi(GpioPin.GPIO1_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        self.write_spi(GpioPin.GPIO1_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRB

        self.write_gpio(GpioPin.GPIO1_SELECT.value, [0, 0, 0, 0, 0, 0, 0, 0], "B")

        self.write_spi(GpioPin.GPIO2_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        self.write_spi(GpioPin.GPIO2_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB

        self.write_spi(GpioPin.GPIO3_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRA
        self.write_spi(GpioPin.GPIO3_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB

        self.write_spi(GpioPin.GPIO4_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        self.write_spi(GpioPin.GPIO4_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1))

    @staticmethod
    def init_gpio():
        # GPIO.init()

        GPIO.setup(Pin.CLK.value, GPIO.OUT)
        GPIO.setup(Pin.MOSI.value, GPIO.OUT)
        GPIO.setup(Pin.MISO.value, GPIO.IN)
        GPIO.setup(Pin.POT_SELECT.value, GPIO.OUT)
        GPIO.setup(Pin.ADC_SELECT.value, GPIO.OUT)
        GPIO.setup(Pin.POWER_DOWN.value, GPIO.OUT)
        GPIO.setup(Pin.GPIO1_SELECT.value, GPIO.OUT)
        GPIO.setup(Pin.GPIO2_SELECT.value, GPIO.OUT)
        GPIO.setup(Pin.GPIO3_SELECT.value, GPIO.OUT)
        GPIO.setup(Pin.GPIO4_SELECT.value, GPIO.OUT)
        GPIO.setup(Pin.ACCESSORY_POWER.value, GPIO.IN)

        GPIO.output(Pin.CLK.value, 0)
        GPIO.output(Pin.MOSI.value, 0)
        GPIO.output(Pin.POT_SELECT.value, 1)
        GPIO.output(Pin.ADC_SELECT.value, 1)
        GPIO.output(Pin.GPIO1_SELECT.value, 1)
        GPIO.output(Pin.GPIO2_SELECT.value, 1)
        GPIO.output(Pin.GPIO3_SELECT.value, 1)
        GPIO.output(Pin.GPIO4_SELECT.value, 1)
        GPIO.output(Pin.POWER_DOWN.value, 0)

    def write_gpio(self, slave, byte, gpio: str):
        # TODO: should probably make some sort of GPIO class abstraction...
        if gpio == "A":
            message = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0] + byte
            self.write_spi(slave, message)  # write GPIO A
        elif gpio == "B":
            message = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1] + byte
            self.write_spi(slave, message)  # write GPIO B
        else:
            raise Exception(f"Invalid GPIO '{gpio}'")

    def read_gpio(self, slave, gpio: str):
        # TODO: should probably make some sort of GPIO class abstraction...
        if gpio == "A":
            message = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
            return self.read_gpio_spi(slave, message)  # write GPIO A
        elif gpio == "B":
            message = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
            return self.read_gpio_spi(slave, message)  # write GPIO B
        else:
            raise Exception(f"Invalid GPIO '{gpio}'")

    def set_pot(self, value):
        value = max(0., min(1., 1. - value))
        message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        self.write_spi(GpioPin.POT_SELECT, message)

    @staticmethod
    def write_spi(slave, message):
        GPIO.output(slave, 0)
        # time.sleep(0.005)
        for entry in message:
            GPIO.output(GpioPin.MOSI, entry)
            GPIO.output(GpioPin.CLK, 1)
            # time.sleep(0.005)
            GPIO.output(GpioPin.CLK, 0)
            # time.sleep(0.005)
        GPIO.output(GpioPin.MOSI, 0)
        GPIO.output(slave, 1)
        # time.sleep(0.005)

    @staticmethod
    def read_adc(channel) -> float:
        read = []
        message = [0, 1, 1]
        bin_channel = int_to_binary(channel)[-3:]
        message += bin_channel
        GPIO.output(GpioPin.ADC_SELECT, 0)
        message = (0, 1, 1, 0, 0, 1)

        for entry in message:
            GPIO.output(GpioPin.MOSI, entry)
            GPIO.output(GpioPin.CLK, 1)
            GPIO.output(GpioPin.CLK, 0)

        for _ in range(12):
            GPIO.output(GpioPin.CLK, 1)
            GPIO.output(GpioPin.CLK, 0)
            read.append(GPIO.input(GpioPin.MISO))

        GPIO.output(GpioPin.ADC_SELECT, 1)
        return binary_to_decimal(read)

    @staticmethod
    def read_gpio_spi(slave, message: tuple):
        GPIO.output(slave, 0)
        # time.sleep(0.005)
        read = []
        for entry in message:
            GPIO.output(GpioPin.MOSI, entry)
            GPIO.output(GpioPin.CLK, 1)
            # time.sleep(0.005)
            GPIO.output(GpioPin.CLK, 0)
            # time.sleep(0.005)
        for entry in range(8):
            GPIO.output(GpioPin.CLK, 1)
            # time.sleep(0.005)
            read.append(GPIO.input(GpioPin.MISO))
            GPIO.output(GpioPin.CLK, 0)
            # time.sleep(0.005)
        GPIO.output(slave, 1)
        # time.sleep(0.005)
        return read


class GPIOHandlerDummy:
    def __init__(self):
        print("WARNING: This is a dummy GPIOHandler class for testing")

    def init_pot(self):
        pass

    def init_xpndr(self):
        pass

    @staticmethod
    def init_gpio():
        pass

    def write_gpio(self, slave, byte, gpio: str):
        pass

    def read_gpio(self, slave, gpio: str):
        pass

    def set_pot(self, value):
        pass

    @staticmethod
    def write_spi(slave, message):
        pass

    @staticmethod
    def read_adc(channel) -> float:
        pass

    @staticmethod
    def read_gpio_spi(slave, message: tuple):
        pass
