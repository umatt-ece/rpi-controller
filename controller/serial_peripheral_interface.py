from controller import GPIOHandler


class SerialPeripheralInterface():
    def __init__(self):
        self.gpio = GPIOHandler()
        self.gpio.init_pins()

    def write_message(self, channel, message):
        print("sending message...")
