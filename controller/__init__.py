# NOTE: order of imports is important to avoid circular references
import os

from .utils import int_to_binary, binary_to_decimal

if os.getenv("LOCAL", "true") == "false":
    from .gpio_handler import GPIOHandler
else:
    # If we are running locally, import a dummy GpioHandler class
    from .gpio_handler import GPIOHandlerDummy as GPIOHandler

from .drive_state_machine import DriveStateMachine
