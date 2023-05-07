import os
import time

from controller import GPIOHandler, SerialPeripheralInterface
from database import DataStore, LiveData as lD


class Controller:
    def __init__(self):
        time.sleep(100)
        self.data_store = DataStore()
        self.gpio = GPIOHandler()
        self.spi = SerialPeripheralInterface()

    def run(self):
        # initialize GpioHandler

        try:
            self.data_store.set(lD.CONTROLLER_ONLINE, True)
            while True:
                # TODO: add initialization functions...
                # self.gpio.init_gpio()
                # self.gpio.init_xpndr()
                # self.gpio.init_pot()
                print("stuff... things... etc...")



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
