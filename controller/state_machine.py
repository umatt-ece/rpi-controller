import time

from controller import GPIOHandler
from database import DataStore, LiveData as lD, StoredData as sD


class StateMachine:
    def __init__(self):
        self.data_store = DataStore()
        self.gpio = GPIOHandler()

        self.last_run = time.perf_counter()
        self.values = {}

        # test:
        self.i = 0

    def update_values(self):
        self.values = self.data_store.get_many([
            lD.GEAR,  # TODO: fetch the values we want from redis for each step...
        ])

    def step(self):
        print(f"step: {self.i}")
        self.i += 1
        pass  # TODO: state machine logic here...

    def run(self):
        if self.last_run + STEP_INTERVAL < time.perf_counter():
            self.last_run = time.perf_counter()
            self.step()


STEP_INTERVAL = 1
