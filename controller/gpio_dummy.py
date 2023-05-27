from typing import Union


class GpioDummy:
    BCM = "BCM"
    IN = "IN"
    OUT = "OUT"

    def __init__(self):
        print("WARNING: This is a dummy Gpio class for testing")
        self.inputs = {}
        self.outputs = {}

    @staticmethod
    def setmode(mode: BCM):
        print(f"GPIO: Mode: {mode}")

    @staticmethod
    def setwarnings(warnings: bool):
        print(f"GPIO: Warnings: {warnings}")

    @staticmethod
    def setup(pin: int, pin_type: Union[IN, OUT]):
        print(f"GPIO: Initializing pin {pin} to type '{pin_type}'")

    @staticmethod
    def input(pin: int):
        return 0

    @staticmethod
    def output(spin: int, value: int):
        pass
