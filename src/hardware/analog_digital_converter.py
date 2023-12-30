import logging

from .interfaces import SerialPeripheralInterface, SpiDevice


class MCP3208(SpiDevice):
    """
    MicroChip Serial Interface (SPI) 12-bit Successive Approximation Analog to Digital Converter device implementation
    for Raspberry Pi.
    """
    SINGLE = "single-ended"
    DIFFERENTIAL = "differential"

    _mode = ""

    def __init__(self, name: str, mode: str = SINGLE) -> None:
        super().__init__(name)
        self._mode = self.validate_mode(mode)

    def set_mode(self, mode: str) -> None:
        self._mode = self.validate_mode(mode)

    def read_analog(self, channel: int) -> int:
        """
        Read the current analog value from the selected device channel. Takes 1 positional argument:

        :param channel: Channel of ADC to read value from (range of values depends on configured mode).
        """
        # Validate
        if self.mode == self.SINGLE and (channel < 0 or channel > 7):
            self._logger.error(f"Channel '{channel}' is invalid for mode '{self.mode}' (must be between 0 to 7")
            raise Exception(f"Channel '{channel}' is invalid for mode '{self.mode}' (must be between 0 to 7")
        if self.mode == self.DIFFERENTIAL and (channel < 0 or channel > 3):
            self._logger.error(f"Channel '{channel}' is invalid for mode '{self.mode}' (must be between 0 to 3")
            raise Exception(f"Channel '{channel}' is invalid for mode '{self.mode}' (must be between 0 to 3")

        # Read analog value
        command_message = f"1{'1' if self._mode == self.SINGLE else '0'}{self.integer_to_binary(channel)}"
        return self.binary_to_integer(self.read(13, message=command_message))

    def validate_mode(self, mode: str) -> str:
        if mode != self.SINGLE or mode != self.DIFFERENTIAL:
            self._logger.error(f"Invalid mode: {mode}")
            raise Exception(f"Invalid mode: {mode}")

        return mode  # If valid, return the string

    @staticmethod
    def binary_to_integer(binary: str) -> int:
        pass

    @staticmethod
    def integer_to_binary(integer: int) -> str:
        return bin(7)[2:]

    @property
    def mode(self) -> str:
        return self._mode


# class AnalogDigitalConverter:
#     def __init__(self):
#         self._gpio = GpioHandler()
#         self._spi = SerialPeripheralInterface()
#
#         self.initialize()
#
#     def initialize(self):
#         self._gpio.init_output(Pin.ADC_SELECT)
#         self._gpio.set(Pin.ADC_SELECT, 1)
#
#     def read(self, channel: int) -> float:
#         read = []
#         message = [0, 1, 1]
#         bin_channel = int_to_binary(channel)[-3:]
#         message += bin_channel
#         self._gpio.set(Pin.ADC_SELECT, 0)
#         message = (0, 0, 0, 1, 1, 0, 0, 1)
#         for entry in message:
#             self._gpio.set(Pin.MOSI, entry)
#             self._gpio.set(Pin.CLK, 1)
#             self._gpio.set(Pin.CLK, 0)
#         self._gpio.set(Pin.MOSI, 0)
#         self._gpio.set(Pin.CLK, 1)
#         self._gpio.set(Pin.CLK, 0)
#         for xx in range(12):
#             self._gpio.set(Pin.CLK, 1)
#             self._gpio.set(Pin.CLK, 0)
#             read.append(self._gpio.read(Pin.MISO))
#
#         self._gpio.set(Pin.ADC_SELECT, 1)
#         print(f"ADC: raw value: {read}")
#         result = binary_to_decimal(read)
#         print(f"ADC: reading: {result}")
#         return result
