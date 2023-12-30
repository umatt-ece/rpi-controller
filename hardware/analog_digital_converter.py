from common import binary_string_to_integer, integer_to_binary_string
from hardware import SpiDevice


class MCP3208(SpiDevice):
    """
    MicroChip Serial Interface (SPI) 12-bit Successive Approximation Analog to Digital Converter device implementation
    for Raspberry Pi.

    SPI Protocol:
     * A 'start' bit is determined as the first clock received where the Select is LOW and Data In (MOSI) is HIGH.
     * The device will begin to sample the analog input on the fourth rising edge of the clock (after start bit).
     * The device will end the sample period on the fifth falling edge of the clock (after start bit).
     * Data is clocked IN  (MOSI) on the 'rising'  edge of the clock signal.
     * Data is clocked OUT (MISO) on the 'falling' edge of the clock signal.
     * Optionally: the message can be padded with leading 0's (to conform to an even number of bytes).

                                    [  CHANNEL   ]         [ ========================= DATA ========================== ]
     [0] ... [0] [Start] [SIG/DIFF] [D2] [D1] [D0] [X] [X] [B11] [B10] [B9] [B8] [B7] [B6] [B5] [B4] [B3] [B2] [B1] [B0]
          |                                           |
      Leading Zero's                          Sample & hold period

    Mode:
     * Single-Ended:
     * Differential:
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
        :return: Integer value of analog value (representation depends on configured mode).
        """
        # Validate
        if self.mode == self.SINGLE and (channel < 0 or channel > 7):
            raise Exception(f"Channel '{channel}' is invalid for mode '{self.mode}' (must be between 0 to 7")
        if self.mode == self.DIFFERENTIAL and (channel < 0 or channel > 3):
            raise Exception(f"Channel '{channel}' is invalid for mode '{self.mode}' (must be between 0 to 3")

        # Read analog value
        command_message = f"01{'1' if self._mode == self.SINGLE else '0'}{integer_to_binary_string(channel)}00"
        return binary_string_to_integer(self.read(12, message=command_message))

    def validate_mode(self, mode: str) -> str:
        """
        Validate that the provided string matches a valid mode for the device. Take 1 positional argument:

        :param mode: String name of the mode.
        :return: Copy of string argument `mode` for convenience (wrapper).
        """
        if mode != self.SINGLE and mode != self.DIFFERENTIAL:
            raise Exception(f"Invalid mode: {mode}")

        return mode  # If valid, return the string

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
