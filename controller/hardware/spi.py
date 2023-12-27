import logging

from controller.hardware import Pin


# class SpiByte(Enum):
#     GPIO_OPCODE_WRITE = [0, 1, 0, 0, 0, 0, 0, 0]
#     GPIO_OPCODE_READ = [0, 1, 0, 0, 0, 0, 0, 1]
#     GPIO_SELECT_IOCON = [0, 0, 0, 0, 1, 0, 1, 0]
#     GPIO_SELECT_DIRA = [0, 0, 0, 0, 0, 0, 0, 0]
#     GPIO_SELECT_DIRB = [0, 0, 0, 0, 0, 0, 0, 1]
#     GPIO_SELECT_PORTA = [0, 0, 0, 1, 0, 0, 1, 0]
#     GPIO_SELECT_PORTB = [0, 0, 0, 1, 0, 0, 1, 1]
#     ALL_OUTPUT = [0, 0, 0, 0, 0, 0, 0, 0]
#     ALL_INPUT = [1, 1, 1, 1, 1, 1, 1, 1]


class SerialPeripheralInterface:
    def __init__(self, select: Pin, clock: Pin, mosi: Pin, miso: Pin, logger: logging.Logger = None) -> None:
        self._logger = logger or logging.getLogger("hardware")
        self._select = select
        self._clock = clock
        self._mosi = mosi
        self._miso = miso

    def write(self, message: str, continue_message: bool = False) -> None:
        print(f"{message}: {continue_message}")
        # Validate Message
        if len(message) % 8 != 0:
            self._logger.error("SPI message must be whole number of bytes (ie. its length must be some multiple of 8)")
        for bit in message:
            if bit != "0" and bit != "1":
                self._logger.error(f"Character '{bit}' is not a valid bit (ie. not '0' or '1')")

        if message[7] == "0":
            self._logger.info(f"Sending Write Message  (address {message[0:7]}): {message}")
        else:
            self._logger.info(f"Sending Read Request   (address {message[0:7]})")

        self._select.write(0)  # Pull Chip Select low to begin transmission

        for bit in message:
            # Write next bit
            if bit == "0":
                self._mosi.write(0)
            elif bit == "1":
                self._mosi.write(0)
            # Toggle clock
            self._clock.write(1)
            self._clock.write(0)

        self._mosi.write(0)  # Clear data line

        if not continue_message:
            self._select.write(1)  # Pull Chip Select high to end transmission

    def read(self, address: str, num_bytes: int, message: str = "") -> str:
        # Validate Message
        if len(address) != 7:
            self._logger.error("SPI address must be 7 bits in length")
        if num_bytes <= 0:
            self._logger.error(f"Cannot read '{num_bytes}' number of bytes")

        message = ""
        self.write(f"{address}1{message}", continue_message=True)

        for bit in range(num_bytes * 8):
            # Toggle clock HIGH
            self._clock.write(1)
            # Read next bit
            message += str(self._miso.read())
            # Toggle clock LOW
            self._clock.write(0)

        self._select.write(1)  # Pull Chip Select high to end transmission

        self._logger.info(f"Received Read Response (address {address}): {message}")
        return message


class SpiDevice:
    _interface = None

    def __init__(self, name: str, address: str, logger: logging.Logger):
        self._logger = logger or logging.getLogger("hardware")
        self._name = name
        self._address = address

    def set_interface(self, interface: SerialPeripheralInterface):
        self._interface = interface

    def write(self, message: str) -> None:
        self._interface.write(f"{self._address}0{message}")

    def read(self, num_bytes: int, message: str = "") -> str:
        return self._interface.read(self._address, num_bytes, message)

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address
