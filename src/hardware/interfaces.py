import logging

from .peripherals import Pin


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

        self._logger.debug(f"Sending Message: {message}")
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
    _address = None
    _interface = None
    _reset = None

    def __init__(self, name: str, logger: logging.Logger = None):
        self._logger = logger or logging.getLogger("hardware")
        self._name = name

    def set_address(self, address: str) -> None:
        self._address = address

    def set_interface(self, interface: SerialPeripheralInterface) -> None:
        self._interface = interface

    def set_reset_pin(self, reset: Pin) -> None:
        self._reset = reset

    def write(self, message: str) -> None:
        self._interface.write(message)

    def read(self, num_bits: int, message: str = "") -> str:
        return self._interface.read(num_bits, message)

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
