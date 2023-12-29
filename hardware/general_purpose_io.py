from enum import Enum

from .interfaces import SpiDevice


class MCP23S17Register(Enum):
    IOCON = "00001010"
    IODIRA = "00000000"
    IODIRB = "00000001"
    GPIOA = "00001010"
    GPIOB = "00010011"


class MCP23S17(SpiDevice):
    """
    MicroChip Serial Interface (SPI) 16-bit I/O Expander device implementation for Raspberry Pi.
    """
    _config = {}
    _pin_state = {
        "A": "00000000",
        "B": "00000000",
    }

    def __init__(self, name: str, address: str, config: dict = None) -> None:
        super().__init__(name, f"0100{address}")

        # Optionally, configure the device on initialization (if `config` provided)
        if config:
            self.configure(config)

    def configure(self, config: dict) -> None:
        """

        """
        message_byte_a = ""
        message_byte_b = ""

        for pin in range(8):
            # Port A
            if config["PORTA"][pin] == "input":
                message_byte_a += "1"
            elif config["PORTA"][pin] == "output":
                message_byte_a += "0"
            else:
                self._logger.error(f"'{config['PORTA'][pin]}' is not a valid pin direction ('input'/'output')")
                raise Exception(f"Invalid pin direction {config['PORTA'][pin]}")
            # Port B
            if config["PORTB"][pin] == "input":
                message_byte_b += "1"
            elif config["PORTB"][pin] == "output":
                message_byte_b += "0"
            else:
                self._logger.error(f"'{config['PORTB'][pin]}' is not a valid pin direction ('input'/'output')")
                raise Exception(f"Invalid pin direction {config['PORTB'][pin]}")

        self.write_io(MCP23S17Register.IOCON, "00000000")

        self._logger.info(f"Configuring device {self._name} Port A: {message_byte_a} (0: output | 1: input | A7-A0)")
        self._logger.info(f"Configuring device {self._name} Port B: {message_byte_a} (0: output | 1: input | B7-B0)")

        self.write_io(MCP23S17Register.IODIRA, message_byte_a)  # Configure Port A
        self.write_io(MCP23S17Register.IODIRB, message_byte_b)  # Configure Port B

    def write_io(self, register: MCP23S17Register, message: str) -> None:
        """
        A wrapper function for SpiDevice.write(). No address  byte is required since that is automatically handled,
        based on the class variable `_address`. Requires 2 position arguments:

        :param register: Enum of type MCP23S17Register that defines the device's register to write to (8-bit address).
        :param message: Message string of bits to write to the device register. String length must be only 1 byte.
        """
        self.write(f"{register.value}{message}")

    def read_io(self, register: MCP23S17Register) -> str:
        """
        A wrapper function for SpiDevice.read(). No address  byte is required since that is automatically handled,
        based on the class variable `_address`. Requires 1 position argument:

        :param register: Enum of type MCP23S17Register that defines the device's register to read from (8-bit address).
        """
        return self.read(1, register.value)

    def write_pin(self, port: str, pin: int, value: bool) -> None:
        """
        Write a value of "1" (True) or "0" (False) to an external GPIO pin. Requires 3 position arguments:

        :param port: Port of MCP23S17 device to write to. Must be either "A" or "b".
        :param pin: Pin number of GPIO port to write to. Must be between 0 and 7.
        :param value: Value to write to GPIO pin. True corresponds to 1/ON and False corresponds to 0/OFF.
        """
        self._logger.info(f"Writing '{'1' if value else '0'}' to {self.name} pin {port}{pin}")

        # Validation
        port = port.upper()
        self._validate_port_pin(port, pin)

        # Construct message
        if port == "A":
            register_byte = MCP23S17Register.GPIOA
            message_byte = f"{self._pin_state['A'][:pin]}{'1' if value else '0'}{self._pin_state['A'][pin + 1:]}"
            self._pin_state["A"] = message_byte  # update pin states
        else:  # Assumed "B" because of previous validation
            register_byte = MCP23S17Register.GPIOB
            message_byte = f"{self._pin_state['B'][:pin]}{'1' if value else '0'}{self._pin_state['B'][pin + 1:]}"
            self._pin_state["A"] = message_byte  # update pin states

        # Send message
        self.write_io(register_byte, message_byte)

    def read_pin(self, port: str, pin: int) -> bool:
        """
        Read the current state ("1"/True or "0"/False) from an external GPIO pin. Requires 2 position arguments:

        :param port: Port of MCP23S17 device to read from. Must be either "A" or "B".
        :param pin: Pin number of GPIO port to read from. Must be between 0 and 7.
        """
        self._logger.info(f"Reading pin {port}{pin} of {self.name}")

        # Validation
        port = port.upper()
        self._validate_port_pin(port, pin)

        # Construct message
        if port == "A":
            register_byte = MCP23S17Register.GPIOA
        else:  # Assumed "B" because of previous validation
            register_byte = MCP23S17Register.GPIOB

        # Send message
        value = self.read_io(register_byte)

        self._logger.info(f"{self.name}: pin {port}{pin} = '{value[pin] == '1'}'")
        return value[pin] == "1"  # return True if "1" or False if "0"

    def _validate_port_pin(self, port: str, pin: int) -> None:
        """
        Validate given `port` and `pin` values and raise an exception if not within expected range.

        :param port: Port value must be either "A" or "B".
        :param pin: Pin value must be between 0 and 7.
        """
        if port != "A" and port != "B":
            self._logger.error(f"'{port}' is not a valid port (must be 'A' or 'B')")
            raise Exception(f"Invalid port value {port}")
        if pin < 0 or pin > 7:
            self._logger.error(f"'{pin}' is not a valid pin (must be between 0 and 7)")
            raise Exception(f"Invalid pin number {pin}")

# class Expander:
#     def __init__(self):
#         self._gpio = GpioHandler()
#         self._spi = SerialPeripheralInterface()
#
#         self.initialize()
#
#     def initialize(self):
#         for pin in [Pin.GPIO1_SELECT, Pin.GPIO2_SELECT, Pin.GPIO3_SELECT, Pin.GPIO4_SELECT]:
#             self._gpio.init_output(pin)
#         for pin in [Pin.GPIO1_SELECT, Pin.GPIO2_SELECT, Pin.GPIO3_SELECT, Pin.GPIO4_SELECT]:
#             self._gpio.set(pin, 1)
#
#         self.init_gpio(Pin.GPIO1_SELECT, SpiByte.ALL_INPUT.value, SpiByte.ALL_OUTPUT.value)  # B -> to relay, A -> sensors
#         # self.init_gpio(Pin.GPIO2_SELECT, SpiByte.ALL_INPUT.value, SpiByte.ALL_INPUT.value)
#         self.init_gpio(Pin.GPIO3_SELECT, SpiByte.ALL_OUTPUT.value, SpiByte.ALL_OUTPUT.value)  # B -> sevcon
#         self.init_gpio(Pin.GPIO4_SELECT, SpiByte.ALL_OUTPUT.value, [0, 0, 1, 1, 1, 1, 1, 1])  # peripherals 'A' and 'B'
#
#     def init_gpio(self, select: Pin, config_a: list[int], config_b: list[int]):
#         self._spi.write(select, SpiByte.GPIO_OPCODE_WRITE.value + SpiByte.GPIO_SELECT_IOCON.value + SpiByte.ALL_OUTPUT.value)
#         self._spi.write(select, SpiByte.GPIO_OPCODE_WRITE.value + SpiByte.GPIO_SELECT_DIRA.value + config_a)  # configure pins on side A
#         self._spi.write(select, SpiByte.GPIO_OPCODE_WRITE.value + SpiByte.GPIO_SELECT_DIRB.value + config_b)  # configure pins on side B
#
#     def read_gpio(self, select: int, side: str) -> list[int]:
#         spi_info = self.get_pin_and_port(select, side)
#         return self._spi.read(spi_info[0], SpiByte.GPIO_OPCODE_READ.value + spi_info[1].value, 8)
#
#     def write_gpio(self, select: int, side: str, message: list[int]):
#         if len(message) != 8:
#             raise Exception(f"ERROR: message must be of size {8} bits but got {len(message)} bits instead")
#         spi_info = self.get_pin_and_port(select, side)
#         message.reverse()
#         self._spi.write(spi_info[0], SpiByte.GPIO_OPCODE_WRITE.value + spi_info[1].value + message)
#
#     @staticmethod
#     def get_pin_and_port(pin: int, port: str) -> [Pin, SpiByte]:
#         if pin == 1 and port == "A":
#             return [Pin.GPIO1_SELECT, SpiByte.GPIO_SELECT_PORTA]
#         elif pin == 1 and port == "B":
#             return [Pin.GPIO1_SELECT, SpiByte.GPIO_SELECT_PORTB]
#         elif pin == 2 and port == "A":
#             return [Pin.GPIO2_SELECT, SpiByte.GPIO_SELECT_PORTA]
#         elif pin == 2 and port == "B":
#             return [Pin.GPIO2_SELECT, SpiByte.GPIO_SELECT_PORTB]
#         elif pin == 3 and port == "A":
#             return [Pin.GPIO3_SELECT, SpiByte.GPIO_SELECT_PORTA]
#         elif pin == 3 and port == "B":
#             return [Pin.GPIO3_SELECT, SpiByte.GPIO_SELECT_PORTB]
#         elif pin == 4 and port == "A":
#             return [Pin.GPIO4_SELECT, SpiByte.GPIO_SELECT_PORTA]
#         elif pin == 4 and port == "B":
#             return [Pin.GPIO4_SELECT, SpiByte.GPIO_SELECT_PORTB]
#         else:
#             raise Exception(f"ERROR: invalid select '{pin}' or side '{port}' for GPIO Expander.")
