import os
import logging

if os.getenv("TESTING", "false") == "false":
    import RPi.GPIO as Gpio
else:
    from hardware import RPiGPIO as Gpio


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
        # Validation
        if direction != "input" and direction != "output":
            self._logger.error(f"'{direction}' is not a valid direction for pin {self._pin_mapping} (must be'input'/'output')")

        # Set direction
        if direction == "input" or direction == "in":
            Gpio.setup(self._pin_mapping, Gpio.IN)
        elif direction == "output" or direction == "out":
            Gpio.setup(self._pin_mapping, Gpio.OUT)

        # Update class variables
        self._pin_direction = direction
        self._logger.info(f"Direction for pin {self._pin_mapping} set to {self._pin_direction}")

    def read(self) -> int:
        value = Gpio.input(self._pin_mapping)
        self._logger.debug(f"{self._pin_mapping} ({self._pin_direction}): {value}")
        return value

    def write(self, value: int) -> None:
        self._logger.debug(f"{self._pin_mapping} ({self._pin_direction}): {value}")
        Gpio.output(self._pin_mapping, value)
    
    @property
    def mapping(self) -> int:
        return self._pin_mapping

    @property
    def direction(self) -> str:
        return self._pin_direction
