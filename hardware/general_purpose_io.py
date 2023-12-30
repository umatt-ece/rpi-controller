from enum import Enum

from common import swap_string_endian
from hardware import Pin, SpiDevice


class MCP23S17Register(Enum):
    IOCON = "00001010"
    IODIRA = "00000000"
    IODIRB = "00000001"
    GPIOA = "00010010"
    GPIOB = "00010011"


class MCP23S17(SpiDevice):
    """
    MicroChip Serial Interface (SPI) 16-bit I/O Expander device implementation for Raspberry Pi.
    """
    PORTA = "PORTA"
    PORTB = "PORTB"

    _config = {}
    _pin_state = {
        "A": "00000000",
        "B": "00000000",
    }

    def __init__(self, name: str, address: str, reset: Pin = None, config: dict = None) -> None:
        super().__init__(name)
        self.set_address(f"0100{swap_string_endian(address)}")

        # Optionally, set rest pin (if `reset` provided)
        if reset:
            self.set_reset_pin(reset)

        # Optionally, configure the device on initialization (if `config` provided)
        if config:
            self.configure(config)

    def configure(self, config: dict, bank: bool = False, haen: bool = True) -> None:
        """  

        """
        message_byte_a = ""
        message_byte_b = ""

        # If a reset pin has been configured, reset the device (otherwise continue with initialization)
        if self._reset:
            self._reset.write(0)
            self._reset.write(1)

        # Construct IO direction bytes based on config
        for pin in range(8):
            # Port A
            if config[self.PORTA][pin] == "input":
                message_byte_a += "1"
            elif config[self.PORTA][pin] == "output":
                message_byte_a += "0"
            else:
                self._logger.error(f"'{config[self.PORTA][pin]}' is not a valid pin direction " +
                                   "('{Pin.INPUT}'/'{Pin.OUTPUT}')")
                raise Exception(f"Invalid pin direction {config[self.PORTA][pin]}")
            # Port B
            if config[self.PORTB][pin] == Pin.INPUT:
                message_byte_b += "1"
            elif config[self.PORTB][pin] == Pin.OUTPUT:
                message_byte_b += "0"
            else:
                self._logger.error(f"'{config[self.PORTB][pin]}' is not a valid pin direction " +
                                   "('{Pin.INPUT}'/'{Pin.OUTPUT}')")
                raise Exception(f"Invalid pin direction {config[self.PORTB][pin]}")

        # Construct IO configuration register byte
        bank_bit = "1" if bank else "0"
        haen_bit = "1" if haen else "0"
        self.write_io(MCP23S17Register.IOCON, f"{bank_bit}00{haen_bit}0000")

        self._logger.info(f"Configuring device {self._name} {self.PORTA}: {message_byte_a} " +
                          "(0: {Pin.OUTPUT} | 1: {Pin.INPUT} | A0-A7)")
        self._logger.info(f"Configuring device {self._name} {self.PORTB}: {message_byte_b} " +
                          "(0: {Pin.OUTPUT} | 1: {Pin.INPUT} | B0-B7)")

        self.write_io(MCP23S17Register.IODIRA, swap_string_endian(message_byte_a))  # Configure Port A
        self.write_io(MCP23S17Register.IODIRB, swap_string_endian(message_byte_b))  # Configure Port B

    def write_io(self, register: MCP23S17Register, message: str) -> None:
        """
        A wrapper function for SpiDevice.write(). Requires 2 position arguments:

        :param register: Enum of type MCP23S17Register that defines the device's register to write to (8-bit address).
        :param message: Message string of bits to write to the device register. String length must be only 1 byte.
        """
        self.write(f"{self.address}0{register.value}{message}")

    def read_io(self, register: MCP23S17Register) -> str:
        """
        A wrapper function for SpiDevice.read(). Requires 1 position argument:

        :param register: Enum of type MCP23S17Register that defines the device's register to read from (8-bit address).
        """
        return self.read(8, f"{self.address}1{register.value}")

    def write_pin(self, port: str, pin: int, value: bool) -> None:
        """
        Write a value of "1" (True) or "0" (False) to an external GPIO pin. Requires 3 position arguments:

        :param port: Port of MCP23S17 device to write to. Must be either "A" or "b".
        :param pin: Pin number of GPIO port to write to. Must be between 0 and 7.
        :param value: Value to write to GPIO pin. True corresponds to 1/ON and False corresponds to 0/OFF.
        """
        self._logger.info(f"{self.name}: Writing '{'1' if value else '0'}' to pin {port}{pin}")

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
        self.write_io(register_byte, swap_string_endian(message_byte))

    def read_pin(self, port: str, pin: int) -> bool:
        """
        Read the current state ("1"/True or "0"/False) from an external GPIO pin. Requires 2 position arguments:

        :param port: Port of MCP23S17 device to read from. Must be either "A" or "B".
        :param pin: Pin number of GPIO port to read from. Must be between 0 and 7.
        """
        self._logger.debug(f"{self.name}: Reading current state of pin {port}{pin}")

        # Validation
        port = port.upper()
        self._validate_port_pin(port, pin)

        # Construct message
        if port == "A":
            register_byte = MCP23S17Register.GPIOA
        else:  # Assumed "B" because of previous validation
            register_byte = MCP23S17Register.GPIOB

        # Send/Receive message
        value = swap_string_endian(self.read_io(register_byte))

        self._logger.info(f"{self.name}: Pin {port}{pin} state is '{value[pin] == '1'}'")
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
