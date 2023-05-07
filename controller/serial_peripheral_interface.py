from controller import GPIOHandler



class SerialPeripheralInterface():
    def __init__(self):
        self.gpio = GPIOHandler()

    def write_message(self, channel, message):
        pass