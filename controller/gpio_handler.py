from enum import Enum
# TODO: the old controller used this library
import RPi.GPIO as GPIO
# TODO: this library supports SPI, maybe also consider pigpio which supports SPI, I2C, and UART
import gpiozero as gpio


class GpioPin(Enum):
    CLK = 23
    MOSI = 10
    MISO = 25
    POT_SELECT = 8
    ADC_SELECT = 5
    POWER_DOWN = 12
    GPIO1_SELECT = 24
    GPIO2_SELECT = 9
    GPIO3_SELECT = 11
    GPIO4_SELECT = 6
    ACCESSORY_POWER = 16


class GPIOHandler:
    def __init__(self):
        pass

    def read_gpio(self, pin: GpioPin):
        pass

    def write_gpio(self, pin: GpioPin, value):
        pass

