import logging
from typing import Union
from random import randint


class RPiGPIO:
    BCM = "BCM"
    BOARD = "BOARD"
    IN = "IN"
    OUT = "OUT"

    def __init__(self):
        print("WARNING: You are currently using a dummy GPIO class `RPiGPIO` designed for integration testing")

    @staticmethod
    def setmode(mode: BCM):
        print(f"RPiGPIO: Mode: {mode}")

    @staticmethod
    def setwarnings(warnings: bool):
        print(f"RPiGPIO: Warnings: {warnings}")

    @staticmethod
    def setup(pin: int, pin_type: Union[IN, OUT]):
        print(f"RPiGPIO: Initializing pin {pin} to type '{pin_type}'")

    @staticmethod
    def input(pin: int):
        return randint(0, 1)

    @staticmethod
    def output(spin: int, value: int):
        pass
