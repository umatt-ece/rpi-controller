import time

from controller import GpioHandler
from database import DataStore, Parameters as Param


class LightsStateMachine:
    def __init__(self):
        self._data_store = DataStore()
        self._gpio = GpioHandler()

        self._last_runtime = time.perf_counter()

        self._headlight_left_state = False
        self._headlight_right_state = False

    def step(self):
        if self._data_store.get(Param.HEADLIGHT_LEFT) != self._headlight_left_state:
            self._headlight_left_state = not self._headlight_left_state
            print("INFO: toggling left headlight")
            # TODO: set headlight pin
        if self._data_store.get(Param.HEADLIGHT_RIGHT) != self._headlight_right_state:
            self._headlight_right_state = not self._headlight_right_state
            print("INFO: toggling right headlight")
            # TODO: set headlight pin

    def run(self):
        if time.perf_counter() >= self._last_runtime + LIGHTS_STEP_INTERVAL:
            self.step()
            self._last_runtime = time.perf_counter()


LIGHTS_STEP_INTERVAL = 1
