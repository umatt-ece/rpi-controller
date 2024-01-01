import logging

from common import validate_binary_string
from hardware import Pin


class SerialPeripheralInterface:
    def __init__(self, select: Pin, clock: Pin, mosi: Pin, miso: Pin, logger: logging.Logger = None) -> None:
        self._logger = logger or logging.getLogger("hardware")
        self._select = select
        self._clock = clock
        self._mosi = mosi
        self._miso = miso

    def write(self, message: str, continue_message: bool = False) -> None:
        # Validate Message
        for bit in message:
            if bit != "0" and bit != "1":
                self._logger.error(f"Character '{bit}' is not a valid bit (ie. not '0' or '1')")
                raise Exception(f"Character '{bit}' is not a valid bit (ie. not '0' or '1')")

        self._logger.info(f"Sending Message: {message}")
        self._select.write(0)  # Pull Chip Select low to begin transmission

        for bit in message:
            # Write next bit
            if bit == "0":
                self._mosi.write(0)
            elif bit == "1":
                self._mosi.write(1)
            # Toggle clock
            self._clock.write(1)
            self._clock.write(0)

        self._mosi.write(0)  # Clear data line

        if not continue_message:
            self._select.write(1)  # Pull Chip Select high to end transmission

    def read(self, num_bits: int, message: str = "") -> str:
        # Validate Message
        if num_bits <= 0:
            self._logger.error(f"Cannot read '{num_bits}' number of bits")
            raise Exception(f"Cannot read '{num_bits}' number of bits")

        # Send read request
        self.write(f"{message}", continue_message=True)

        # Read device response
        response = ""
        for bit in range(num_bits):
            # Toggle clock HIGH
            self._clock.write(1)
            # Read next bit
            response += str(self._miso.read())
            # Toggle clock LOW
            self._clock.write(0)

        self._select.write(1)  # Pull Chip Select high to end transmission

        self._logger.debug(f"Received Message: {response}")
        return response


class SpiDevice:
    """
    SpiDevice acts as an 'interface' class for all SPI protocol devices. It is not intended to be implemented itself,
    but rather be the Parent of some other class that implements the details of the device. It contains a number of
    generic class parameters (`address` and `reset`) which can be implemented depending on the type of device (but are
    not required).
    """
    _interface = None
    _address = None
    _reset = None
    _shutdown = None

    def __init__(self, name: str, logger: logging.Logger = None) -> None:
        self._logger = logger or logging.getLogger("hardware")
        self._name = name

    def set_interface(self, interface: SerialPeripheralInterface) -> None:
        """
        Setter function for required class variable `interface`. Takes 1 positional argument:

        :param interface: Interface to assign to the device (must be a valid SerialPeripheralInterface class instance).
        """
        self._interface = interface

    def set_address(self, address: str) -> None:
        """
        Setter function for optional class variable `address`. Takes 1 positional argument:

        :param address: Address to assign to the device (must be a binary string).
        """
        self._address = validate_binary_string(address)

    def set_reset_pin(self, reset: Pin) -> None:
        """
        Setter function for optional class variable `reset`. Takes 1 positional argument:

        :param reset: Reset pin to assign to the device (must be a valid Pin class instance).
        """
        self._reset = reset

    def set_shutdown_pin(self, shutdown: Pin) -> None:
        """
        Setter function for optional class variable `shutdown`. Takes 1 positional argument:

        :param shutdown: Shutdown pin to assign to the device (must be a valid Pin class instance).
        """
        self._shutdown = shutdown

    def write(self, message: str) -> None:
        """
        Wrapper function for `SerialPeripheralInterface.write()`.
        """
        if self._interface:
            self._interface.write(message)
        else:
            self._logger.error(f"Cannot write to '{self.name}', no interface (call `set_interface` and try again.")

    def read(self, num_bits: int, message: str = "") -> str:
        """
        Wrapper function for `SerialPeripheralInterface.read()`.
        """
        if self._interface:
            return self._interface.read(num_bits, message)
        else:
            self._logger.error(f"Cannot read from '{self.name}', no interface (call `set_interface` and try again.")

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address


class InterIntegratedCircuit:
    # TODO: Implement I2C protocol
    pass


class I2cDevice:
    # TODO: Implement I2C device
    pass


class ControllerAreaNetwork:
    # TODO: Implement CAN protocol
    pass


class CanDevice:
    # TODO: Implement CAN device
    pass
