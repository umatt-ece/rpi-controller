

class AnalogDigitalConverter:
    def __init__(self):
        self._gpio = GpioHandler()
        self._spi = SerialPeripheralInterface()

        self.initialize()

    def initialize(self):
        self._gpio.init_output(Pin.ADC_SELECT)
        self._gpio.set(Pin.ADC_SELECT, 1)

    def read(self, channel: int) -> float:
        read = []
        message = [0, 1, 1]
        bin_channel = int_to_binary(channel)[-3:]
        message += bin_channel
        self._gpio.set(Pin.ADC_SELECT, 0)
        message = (0, 0, 0, 1, 1, 0, 0, 1)
        for entry in message:
            self._gpio.set(Pin.MOSI, entry)
            self._gpio.set(Pin.CLK, 1)
            self._gpio.set(Pin.CLK, 0)
        self._gpio.set(Pin.MOSI, 0)
        self._gpio.set(Pin.CLK, 1)
        self._gpio.set(Pin.CLK, 0)
        for xx in range(12):
            self._gpio.set(Pin.CLK, 1)
            self._gpio.set(Pin.CLK, 0)
            read.append(self._gpio.read(Pin.MISO))

        self._gpio.set(Pin.ADC_SELECT, 1)
        print(f"ADC: raw value: {read}")
        result = binary_to_decimal(read)
        print(f"ADC: reading: {result}")
        return result
