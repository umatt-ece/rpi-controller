# NOTE: order of imports is important to avoid circular references
import os

from .utils import int_to_binary, binary_to_decimal

if os.getenv("LOCAL", "true") == "false":
    print("test")
    from .gpio_handler import GpioPin, GPIOHandler
else:
    from .gpio_handler import GpioPin, GPIOHandlerDummy as GPIOHandler

from .state_machine import StateMachine
