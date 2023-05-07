import os
import time

from controller import StateMachine, GPIOHandler
from database import DataStore, LiveData as lD


class Controller:
    def __init__(self):
        self.data_store = DataStore()
        self.gpio = GPIOHandler()
        # self.state_machine = StateMachine()

    def run(self):

        try:
            self.data_store.set(lD.CONTROLLER_ONLINE, True)
            while True:
                # TODO: add initialization functions...
                # self.gpio.init_gpio()
                # self.gpio.init_xpndr()
                # self.gpio.init_pot()
                self.gpio.test_setup()

                self.gpio.test_run()
                time.sleep(0.1)
                # self.state_machine.run()
                # TODO: add other run functions...

        except Exception as e:
            # TODO: log exceptions first...
            self.data_store.set(lD.CONTROLLER_ONLINE, False)  # this may fail
            raise e  # raise the error anyway so the system can crash


if __name__ == "__main__":
    umatt_controller_application = Controller()
    umatt_controller_application.run()
