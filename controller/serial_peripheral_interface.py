from controller import GPIOHandler
from common import RpiPin as Pin


class SerialPeripheralInterface():
    def __init__(self):
        self.gpio = GPIOHandler()
        self.gpio.init_pins()

    def write_message(self, channel: Pin, message: list[int]):
        print(f"sending message: {message}")
        self.gpio.set_pin(channel, 0)
        # time.sleep(0.005)
        for entry in message:
            self.gpio.set_pin(Pin.MOSI, entry)
            self.gpio.set_pin(Pin.CLK, 1)
            # time.sleep(0.005)
            self.gpio.set_pin(Pin.CLK, 0)
            # time.sleep(0.005)
        self.gpio.set_pin(Pin.MOSI, 0)
        self.gpio.set_pin(channel, 1)
        # time.sleep(0.005)

    def read_message(self, channel: Pin, message: list[int], bits: int) -> list:
        read = []
        self.gpio.set_pin(channel, 0)
        for entry in message:
            self.gpio.set_pin(Pin.MOSI, entry)
            self.gpio.set_pin(Pin.CLK, 1)
            # time.sleep(0.005)
            self.gpio.set_pin(Pin.CLK, 0)
            # time.sleep(0.005)
        for entry in range(bits):
            self.gpio.set_pin(Pin.CLK, 1)
            # time.sleep(0.005)
            read.append(self.gpio.read_pin(Pin.MISO))
            self.gpio.set_pin(Pin.CLK, 0)
            # time.sleep(0.005)
        self.gpio.set_pin(channel, 1)
        # time.sleep(0.005)
        return message
