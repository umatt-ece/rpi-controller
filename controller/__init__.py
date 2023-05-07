# NOTE: order of imports is important to avoid circular references
import os

if os.getenv("LOCAL", "true") == "false":
    from .gpio_handler import GPIOHandler
else:
    # If we are running locally, import a dummy GpioHandler class
    from .gpio_handler import GPIOHandlerDummy as GPIOHandler

from .drive_state_machine import DriveStateMachine
