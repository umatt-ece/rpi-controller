import logging

from logic import BaseStateMachine, DEFAULT_INTERVAL
from hardware import RaspberryPi
from database import DataStore, Parameter


class DemoStateMachine(BaseStateMachine):
    """
    Demo State Machine.
    """
    HOLD = "hold"
    BLINK = "blink"

    NUM_LEDS = 4

    _blink = False
    _counter = 0

    def __init__(self, name: str, rpi: RaspberryPi, datastore: DataStore, initial_state: str = HOLD,
                 interval: int = DEFAULT_INTERVAL, logger: logging.Logger = None):
        super().__init__(name=name, initial_state=initial_state, interval=interval, logger=logger)
        self._rpi = rpi
        self._store = datastore

        self.initialize()

    def initialize(self):
        self._blink = False
        self._counter = 0

    def is_blinking(self):
        return self._blink

    def start_blinking(self):
        self._logger.info("start blinking")
        self._blink = True

    def stop_blinking(self):
        self._logger.info("stop blinking")
        self._blink = False

    def condition_blink(self):
        return self._blink

    def condition_hold(self):
        return not self._blink

    def _turn_on_next_led(self):
        self._logger.info(f"toggling next LED ({self._counter})")
        if self._counter >= self.NUM_LEDS:
            self._counter = 0

        self._rpi.devices["gpio_0"].write_pin(port="A", pin=(self._counter * 2 + 1), value=True)
        if self._counter > 0:
            self._rpi.devices["gpio_0"].write_pin(port="A", pin=((self._counter - 1) * 2 + 1), value=False)
        else:
            self._rpi.devices["gpio_0"].write_pin(port="A", pin=((self.NUM_LEDS - 1) * 2 + 1), value=False)

        self._counter += 1

    def _turn_off_leds(self):
        self._logger.info(f"turning off all LEDs")
        self._rpi.devices["gpio_0"].write_pin(port="A", pin=1, value=False)
        self._rpi.devices["gpio_0"].write_pin(port="A", pin=3, value=False)
        self._rpi.devices["gpio_0"].write_pin(port="A", pin=5, value=False)
        self._rpi.devices["gpio_0"].write_pin(port="A", pin=7, value=False)
        self._counter = 0

    def update(self):
        pass

    def step(self):
        if self._state == self.BLINK:
            self._turn_on_next_led()

    def states(self) -> dict:
        return {
            self.HOLD: {
                "on_enter": [self._turn_off_leds],
                "on_exit": {},
                "transitions": {
                    "transition": {
                        "next_state": self.BLINK,
                        "conditions": [self.condition_blink],
                    }
                }
            },
            self.BLINK: {
                "on_enter": [self._turn_on_next_led],
                "on_exit": {},
                "transitions": {
                    "transition": {
                        "next_state": self.HOLD,
                        "conditions": [self.condition_hold],
                    }
                }
            },
        }
