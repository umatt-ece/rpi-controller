import logging
from typing import Union
from random import randint

print_info = False


class RPiGPIO:
    BCM = "BCM"
    BOARD = "BOARD"
    IN = "IN"
    OUT = "OUT"

    def __init__(self):
        print("WARNING: You are currently using a dummy GPIO class `RPiGPIO` designed for integration testing")

    @staticmethod
    def setmode(mode: BCM):
        if print_info:
            print(f"RPiGPIO: Mode: {mode}")

    @staticmethod
    def setwarnings(warnings: bool):
        if print_info:
            print(f"RPiGPIO: Warnings: {warnings}")

    @staticmethod
    def setup(pin: int, pin_type: Union[IN, OUT]):
        if print_info:
            print(f"RPiGPIO: Initializing pin {pin} to type '{pin_type}'")

    @staticmethod
    def input(pin: int):
        if print_info:
            print(f"RPiGPIO: [read] pin {pin}")
        return randint(0, 1)

    @staticmethod
    def output(pin: int, value: int):
        if print_info:
            print(f"RPiGPIO: [write] pin {pin} = {value}")
