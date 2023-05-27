from typing import Union


class GpioDummy:
    BCM = None
    IN = None
    OUT = None

    def __init__(self):
        print("WARNING: This is a dummy Gpio class for testing")

    @staticmethod
    def setmode(bcm: BCM):
        pass

    @staticmethod
    def setwarnings(warnings: bool):
        pass

    @staticmethod
    def setup(pin: int, pin_type: Union[IN, OUT]):
        pass

    @staticmethod
    def input(pin: int):
        return 0

    @staticmethod
    def output(pin: int, value: int):
        pass
