from enum import Enum
import os

if os.getenv("LOCAL", "true") == "false":
    import RPi.GPIO as GPIO
else:
    # If we are running locally, import a dummy gpio class
    from .gpio_dummy import GpioDummy as GPIO

# TODO: this library supports SPI, maybe also consider pigpio which supports SPI, I2C, and UART
# import gpiozero as gpio


class RpiPin(Enum):
    CLK = 23  # clock for Serial Peripheral Interface (communication protocol) I think...
    MOSI = 10  # 'master out slave in' for SPI
    MISO = 25  # 'master in slave out' for SPI
    POT_SELECT = 8  # Potentiometer
    ADC_SELECT = 5  # Analog Digital Converter
    POWER_DOWN = 12  # Tractor Power
    GPIO1_SELECT = 24
    GPIO2_SELECT = 9
    GPIO3_SELECT = 11
    GPIO4_SELECT = 6
    ACCESSORY_POWER = 16


class GpioHandler:
    Pin = RpiPin

    def __init__(self):
        print("Initializing GPIO Handler...")
        GPIO.setmode(GPIO.BCM)  # use BCM mapping
        GPIO.setwarnings(False)  # ignore warnings

    @staticmethod
    def init_input(pin: Pin):
        GPIO.setup(pin.value, GPIO.IN)

    @staticmethod
    def init_output(pin: Pin):
        GPIO.setup(pin.value, GPIO.OUT)

    @staticmethod
    def read(pin: Pin):
        return GPIO.input(pin.value)

    @staticmethod
    def set(pin: Pin, value):
        GPIO.output(pin.value, value)
