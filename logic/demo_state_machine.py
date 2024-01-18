import logging

from logic import BaseStateMachine, DEFAULT_INTERVAL
from hardware import RaspberryPi
from database import DataStore, Parameter


class DemoStateMachine(BaseStateMachine):
    """
    Demo State Machine.
    """
    DEFAULT = "default"

    def __init__(self, name: str, rpi: RaspberryPi, datastore: DataStore, initial_state: str = DEFAULT,
                 interval: int = DEFAULT_INTERVAL, logger: logging.Logger = None):
        super().__init__(name=name, initial_state=initial_state, interval=interval, logger=logger)
        self._rpi = rpi
        self._store = datastore

        self.initialize()

    def initialize(self):
        pass

    def update(self):
        pass

    def step(self):
        pass

    def states(self) -> dict:
        return {
            self.DEFAULT: {
                "on_enter": [],
                "on_exit": {},
                "transitions": {
                    "transition": {
                        "next_state": None,
                        "conditions": [],
                    }
                }
            },
        }
