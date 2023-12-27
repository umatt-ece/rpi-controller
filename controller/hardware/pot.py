

class Potentiometer:
    def __init__(self):
        self._gpio = GpioHandler()
        self._spi = SerialPeripheralInterface()

        self.initialize()

    def initialize(self):
        self._gpio.init_output(Pin.POT_SELECT)
        self._gpio.set(Pin.POT_SELECT, 1)

        self.write_spi(1.0)

    def set(self, value: float):
        value = max(0.0, min(1.0, 1.0 - value))
        self.write_spi(value)

    def write_spi(self, value: float):
        message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        self._spi.write(Pin.POT_SELECT, message)
