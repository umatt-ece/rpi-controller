import os
import logging

if os.getenv("LOCAL", "true") == "false":
    import RPi.GPIO as Gpio
else:
    from controller.hardware import RPiGPIO as Gpio


class Pin:
    def __init__(self, mapping: int, direction: str = "", logger: logging.Logger = None) -> None:
        self._logger = logger or logging.getLogger("hardware")
        self._pin_mapping = mapping
        self._pin_direction = direction

        if direction:
            self.set_direction(direction.lower())

    @staticmethod
    def configure():
        Gpio.setmode(Gpio.BOARD)  # Use BCM mapping
        Gpio.setwarnings(False)   # Ignore warnings

    def set_direction(self, direction: str) -> None:
        if direction == "input" or direction == "in":
            Gpio.setup(self._pin_mapping, Gpio.IN)
        elif direction == "output" or direction == "out":
            Gpio.setup(self._pin_mapping, Gpio.OUT)
        else:
            self._logger.warning(f"Direction '{direction}' is unknown. Pin {self._pin_mapping} not configured")

    def read(self) -> int:
        return Gpio.input(self._pin_mapping)

    def write(self, value: int) -> None:
        Gpio.output(self._pin_mapping, value)
