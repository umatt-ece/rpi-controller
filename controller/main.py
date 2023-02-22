from database import DataStore


class Controller: # this might not need to be a Class (to be determined later)

    def __init__(self):
        # Initialize global variables
        self.datastore = DataStore()
        # Setup
        pass
    def run(self):

        try:

            while True:
                # execute code (spin up threads ?)
                pass

        except Exception as e:
            # log exceptions

            # raise the error anyway so the system can crash
            raise e


if __name__ == "__main__":
    umatt_controller = Controller()
    umatt_controller.run()
