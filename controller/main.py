from controller import StateMachine
from database import DataStore, LiveData as lD


class Controller:
    def __init__(self):
        self.data_store = DataStore()
        self.state_machine = StateMachine()

    def run(self):

        try:
            self.data_store.set(lD.CONTROLLER_ONLINE, True)
            while True:

                # TODO: add initialization functions...
                # initGPIO()
                # initXPNDR()
                # initPot()

                # self.state_machine.init()
                self.state_machine.run()
                # TODO: add other run functions...

        except Exception as e:
            # TODO: log exceptions first...
            self.data_store.set(lD.CONTROLLER_ONLINE, False)
            raise e  # raise the error anyway so the system can crash


if __name__ == "__main__":
    umatt_controller_application = Controller()
    umatt_controller_application.run()
