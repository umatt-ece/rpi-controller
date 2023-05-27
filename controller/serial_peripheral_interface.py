import time
from enum import Enum

from controller import RpiPin as Pin
from controller import GpioHandler


class SpiByte(Enum):
    GPIO_OPCODE_WRITE = [0, 1, 0, 0, 0, 0, 0, 0]
    GPIO_OPCODE_READ = [0, 1, 0, 0, 0, 0, 0, 1]
    GPIO_SELECT_IOCON = [0, 0, 0, 0, 1, 0, 1, 0]
    GPIO_SELECT_DIRA = [0, 0, 0, 0, 0, 0, 0, 0]
    GPIO_SELECT_DIRB = [0, 0, 0, 0, 0, 0, 0, 1]
    GPIO_SELECT_PORTA = [0, 0, 0, 1, 0, 0, 1, 0]
    GPIO_SELECT_PORTB = [0, 0, 0, 1, 0, 0, 1, 1]
    ALL_OUTPUT = [0, 0, 0, 0, 0, 0, 0, 0]
    ALL_INPUT = [1, 1, 1, 1, 1, 1, 1, 1]


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
        print(f"SPI: sending message: {message}")
        self._gpio.set(channel, 0)
        for entry in message:
            self._gpio.set(Pin.MOSI, entry)
            self._gpio.set(Pin.CLK, 1)
            self._gpio.set(Pin.CLK, 0)
        self._gpio.set(Pin.MOSI, 0)
        self._gpio.set(channel, 1)

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
        # read.reverse()  # ?
        print(f"SPI: reading message: {read}")
        return read
