from controller import DriveStateMachine, LightsStateMachine
from database import DataStore, Parameters


def main():
    try:
        print("Controller starting up...")
        data_store = DataStore()
        drive_state_machine = DriveStateMachine()
        lights_state_machine = LightsStateMachine()

        data_store.set(Parameters.CONTROLLER_ONLINE, True)
        print("Controller ONLINE")
        while True:
            drive_state_machine.run()
            lights_state_machine.run()

    except Exception as e:
        # TODO: log exceptions first...
        data_store.set(Parameters.CONTROLLER_ONLINE, False)  # this may fail
        raise e  # raise the error anyway so the system can crash


if __name__ == "__main__":
    main()
