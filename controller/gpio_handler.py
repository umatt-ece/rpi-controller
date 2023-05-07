from enum import Enum

from database import DataStore, LiveData as lD, StoredData as sD
from common import RpiPin as Pin, int_to_binary, binary_to_decimal

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

    @staticmethod
    def init_input(pin: Pin):
        GPIO.setup(pin.value, GPIO.IN)

    @staticmethod
    def init_output(pin: Pin):
        GPIO.setup(pin.value, GPIO.OUT)

    @staticmethod
    def read_pin(pin: Pin):
        return GPIO.input(pin.value)

    @staticmethod
    def set_pin(pin: Pin, value):
        GPIO.output(pin.value, value)

    def init_pot(self):
        # value = 1.0
        # message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        # self.write_spi(pin.POT_SELECT.value, message)
        pass

    def init_xpndr(self):
        # self.write_spi(GpioPin.GPIO1_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        # self.write_spi(GpioPin.GPIO1_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRB
        #
        # self.write_gpio(GpioPin.GPIO1_SELECT.value, [0, 0, 0, 0, 0, 0, 0, 0], "B")
        #
        # self.write_spi(GpioPin.GPIO2_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        # self.write_spi(GpioPin.GPIO2_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB
        #
        # self.write_spi(GpioPin.GPIO3_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRA
        # self.write_spi(GpioPin.GPIO3_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB
        #
        # self.write_spi(GpioPin.GPIO4_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        # self.write_spi(GpioPin.GPIO4_SELECT.value, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1))
        pass

    def init_pins(self):
        # initial
        for pin in [Pin.CLK, Pin.MOSI, Pin.POT_SELECT, Pin.ADC_SELECT, Pin.POWER_DOWN, Pin.GPIO1_SELECT, Pin.GPIO2_SELECT, Pin.GPIO3_SELECT, Pin.GPIO4_SELECT]:
            self.init_output(pin)
        for pin in [Pin.MISO, Pin.ACCESSORY_POWER]:
            self.init_input(pin)

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
        # # TODO: should probably make some sort of GPIO class abstraction...
        # if gpio == "A":
        #     message = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0] + byte
        #     self.write_spi(slave, message)  # write GPIO A
        # elif gpio == "B":
        #     message = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1] + byte
        #     self.write_spi(slave, message)  # write GPIO B
        # else:
        #     raise Exception(f"Invalid GPIO '{gpio}'")
        pass

    def read_gpio(self, slave, gpio: str):
        # # TODO: should probably make some sort of GPIO class abstraction...
        # if gpio == "A":
        #     message = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        #     return self.read_gpio_spi(slave, message)  # write GPIO A
        # elif gpio == "B":
        #     message = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
        #     return self.read_gpio_spi(slave, message)  # write GPIO B
        # else:
        #     raise Exception(f"Invalid GPIO '{gpio}'")
        pass

    def set_pot(self, value):
        # value = max(0., min(1., 1. - value))
        # message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        # self.write_spi(GpioPin.POT_SELECT, message)
        pass

    @staticmethod
    def write_spi(slave, message):
        # GPIO.output(slave, 0)
        # # time.sleep(0.005)
        # for entry in message:
        #     GPIO.output(GpioPin.MOSI, entry)
        #     GPIO.output(GpioPin.CLK, 1)
        #     # time.sleep(0.005)
        #     GPIO.output(GpioPin.CLK, 0)
        #     # time.sleep(0.005)
        # GPIO.output(GpioPin.MOSI, 0)
        # GPIO.output(slave, 1)
        # # time.sleep(0.005)
        pass

    @staticmethod
    def read_adc(channel) -> float:
        # read = []
        # message = [0, 1, 1]
        # bin_channel = int_to_binary(channel)[-3:]
        # message += bin_channel
        # GPIO.output(GpioPin.ADC_SELECT, 0)
        # message = (0, 1, 1, 0, 0, 1)
        #
        # for entry in message:
        #     GPIO.output(GpioPin.MOSI, entry)
        #     GPIO.output(GpioPin.CLK, 1)
        #     GPIO.output(GpioPin.CLK, 0)
        #
        # for _ in range(12):
        #     GPIO.output(GpioPin.CLK, 1)
        #     GPIO.output(GpioPin.CLK, 0)
        #     read.append(GPIO.input(GpioPin.MISO))
        #
        # GPIO.output(GpioPin.ADC_SELECT, 1)
        # return binary_to_decimal(read)
        pass

    @staticmethod
    def read_gpio_spi(slave, message: tuple):
        # GPIO.output(slave, 0)
        # # time.sleep(0.005)
        # read = []
        # for entry in message:
        #     GPIO.output(GpioPin.MOSI, entry)
        #     GPIO.output(GpioPin.CLK, 1)
        #     # time.sleep(0.005)
        #     GPIO.output(GpioPin.CLK, 0)
        #     # time.sleep(0.005)
        # for entry in range(8):
        #     GPIO.output(GpioPin.CLK, 1)
        #     # time.sleep(0.005)
        #     read.append(GPIO.input(GpioPin.MISO))
        #     GPIO.output(GpioPin.CLK, 0)
        #     # time.sleep(0.005)
        # GPIO.output(slave, 1)
        # # time.sleep(0.005)
        # return read
        pass


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
