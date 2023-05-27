import time
from enum import Enum

from controller import RpiPin as Pin
from controller import GpioHandler


class SpiByte(Enum):
    READ = []
    WRITE = []
    FFFF = []


class SerialPeripheralInterface:
    def __init__(self):
        self._gpio = GpioHandler()

        self.initialize()

    def initialize(self):
        self._gpio.init_output(Pin.CLK)
        self._gpio.init_output(Pin.MOSI)
        self._gpio.init_input(Pin.MISO)

        self._gpio.set(Pin.CLK, 0)
        self._gpio.set(Pin.MOSI, 0)

    def write(self, channel: Pin, message: list[int]):
        print(f"sending message: {message}")
        self._gpio.set(channel, 0)
        time.sleep(0.005)
        for entry in message:
            self._gpio.set(Pin.MOSI, entry)
            self._gpio.set(Pin.CLK, 1)
            time.sleep(0.005)
            self._gpio.set(Pin.CLK, 0)
            time.sleep(0.005)
        self._gpio.set(Pin.MOSI, 0)
        self._gpio.set(channel, 1)
        time.sleep(0.005)

    def read(self, channel: Pin, message: list[int], bits: int) -> list:
        read = []
        self._gpio.set(channel, 0)
        for entry in message:
            self._gpio.set(Pin.MOSI, entry)
            self._gpio.set(Pin.CLK, 1)
            self._gpio.set(Pin.CLK, 0)
        for entry in range(bits):
            self._gpio.set(Pin.CLK, 1)
            read.append(self._gpio.read(Pin.MISO))
            self._gpio.set(Pin.CLK, 0)

        self._gpio.set(channel, 1)
        return message
