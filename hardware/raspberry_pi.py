import logging
import math
from enum import Enum

from hardware import Pin, SerialPeripheralInterface, SpiDevice

J_HEADER_PINS = 40


class RPiModel(Enum):
    RPI3B = "RPI3B"
    RPI4B = "RPI4B"


class RaspberryPi:
    _pinout = {}
    _spi_config = {}
    _i2c_config = {}  # TODO: add I2C implementation
    _can_config = {}  # TODO: add CAN implementation
    _devices = {}

    def __init__(self, model: RPiModel, logger: logging.Logger = None) -> None:
        self._logger = logger or logging.getLogger("hardware")
        self._model = model

        self._initialize_pinout()

    def _initialize_pinout(self) -> None:
        self._pinout = dict(
            [(pin, {
                "pin": Pin(pin),
                "pin_bcm": pinout_mapping[self._model][pin][0],
                "pin_type": pinout_mapping[self._model][pin][1],
                "pin_function": pinout_mapping[self._model][pin][2],
                "pin_description": pinout_mapping[self._model][pin][3],
            }) for pin in range(1, J_HEADER_PINS + 1)]
        )

        Pin.configure()  # Configure pin mapping and warnings

    def _parse_pin(self, name: str) -> int:
        if name.isnumeric():
            return int(name)
        else:
            bcm_length = 0
            while name[-(bcm_length + 1)].isnumeric():
                bcm_length += 1
            pin_type = name[:-bcm_length].upper() if bcm_length > 0 else name.upper()
            pin_bcm = int(name[-bcm_length:]) if bcm_length > 0 else None
        for pin_number in range(1, J_HEADER_PINS + 1):
            if self._pinout[pin_number]['pin_type'] == pin_type and self._pinout[pin_number]['pin_bcm'] == pin_bcm:
                return pin_number
        self._logger.error(f"Could not parse pin name '{name}' to any pins on Raspberry Pi board")
        raise KeyError(f"Could not parse pin name '{name}' to any pins on Raspberry Pi board")

    def configure_spi(self, clock: str, mosi: str, miso: str) -> None:
        self._spi_config = {
            "clock": self._parse_pin(clock),
            "mosi": self._parse_pin(mosi),
            "miso": self._parse_pin(miso),
        }

        # Initialize Clock, MOSI, and MISO pins
        self._pinout[self._spi_config["clock"]]["pin"].set_direction("output")
        self._pinout[self._spi_config["mosi"]]["pin"].set_direction("output")
        self._pinout[self._spi_config["miso"]]["pin"].set_direction("input")

    def add_spi_device(self, device: SpiDevice, select: str, reset: str = "") -> None:
        # Verify that Clock, MOSI, and MISO have already been configured
        if not self._spi_config:
            self._logger.error("No SPI configuration. Please ensure `configure_spi` has been called")

        if reset:
            self._pinout[self._parse_pin(reset)]["pin"].set_direction("output")
            self._pinout[self._parse_pin(reset)]["pin"].write(1)
            device.set_reset_pin(self._pinout[self._parse_pin(reset)]["pin"])

        # Configure an interface (SPI) for added device. Use RPi's Clock, MOSI, and MISO pins & device's Select pin
        device.set_interface(SerialPeripheralInterface(
            self._pinout[self._parse_pin(select)]["pin"],
            self._pinout[self._spi_config["clock"]]["pin"],
            self._pinout[self._spi_config["mosi"]]["pin"],
            self._pinout[self._spi_config["miso"]]["pin"],
        ))

        # Initialize Select pin
        self._pinout[self._parse_pin(select)]["pin"].set_direction("output")
        self._pinout[self._parse_pin(select)]["pin"].write(1)
        # Add new SPI device to list of devices
        self._devices[device.name] = device

    def pin(self, pin: str) -> str:
        # parse the string name to pin_number
        pin = self._parse_pin(pin)

        pin_string = f"{pin}: {self._pinout[pin]['pin_type']}"
        pin_string += f"{self._pinout[pin]['pin_bcm'] if self._pinout[pin]['pin_bcm'] else ''} "
        pin_string += f"({self._pinout[pin]['pin_function']})"

        print(pin_string)  # print string to console
        return pin_string  # additionally return it

    def pinout(self, header: bool = False, margin: int = 30) -> str:
        pinout_string = ""
        # Print 'HEADER'
        if header:
            # determine header sizing
            header_length = (margin - 1) * 2 + 9
            header_padding = (header_length - (len(self._model.value) + 30)) / 2
            #
            pinout_string += f"┏{'━' * header_length}┓\n"
            pinout_string += f"┃{' ' * math.floor(header_padding)}Raspberry Pi ({self._model.value})"
            pinout_string += f" Pinout Mapping{' ' * math.ceil(header_padding)}┃\n"
            pinout_string += f"┗{'━' * header_length}┛\n"
        # Print 'PINOUT'
        pinout_string += f"{' ' * margin}┏━━━━━━━┓\n"
        for pin_number in range(1, J_HEADER_PINS + 1):
            if pin_number % 2 == 1:  # odd pins (left)
                line = f"[{self._pinout[pin_number]['pin_function']}] {self._pinout[pin_number]['pin_type']}"
                line += f"{self._pinout[pin_number]['pin_bcm']}" if self._pinout[pin_number]['pin_bcm'] else ""
                pinout_string += f"{' ' * (margin - len(line) - 1)}{line} ┃ {pin_number}{' ' if pin_number < 10 else ''} "
            else:  # even pins (right)
                line = f"{' ' if pin_number < 10 else ''}{pin_number} ┃ {self._pinout[pin_number]['pin_type']}"
                line += f"{self._pinout[pin_number]['pin_bcm']}" if self._pinout[pin_number]['pin_bcm'] else ""
                pinout_string += f"{line} [{self._pinout[pin_number]['pin_function']}]\n"
        pinout_string += f"{' ' * margin}┗━━━━━━━┛\n"

        print(pinout_string)  # print string to console
        return pinout_string  # additionally return it

    @property
    def devices(self):
        return self._devices


pinout_mapping = {
    RPiModel.RPI4B: {
        # BOARD: [BCM, TYPE, FUNTION, DESCRIPTION]
        1: [None, "PWR", "3V3", "3.3V Power"],
        2: [None, "PWR", "5V", "5V Power"],
        3: [2, "GPIO", "SDA", "General Purpose I/O (I2C Serial Data)"],
        4: [None, "PWR", "5V", "5V Power"],
        5: [3, "GPIO", "SCL", "General Purpose I/O (I2C Serial Clock)"],
        6: [None, "GND", "GND", "Ground"],
        7: [4, "GPIO", "GCLK", "General Purpose I/O ()"],
        8: [14, "GPIO", "TXD", "General Purpose I/O (Transmit)"],
        9: [None, "GND", "GND", "Ground"],
        10: [15, "GPIO", "RXD", "General Purpose I/O (Receive)"],
        11: [17, "GPIO", "GEN0", "General Purpose I/O ()"],
        12: [18, "GPIO", "GEN1", "General Purpose I/O ()"],
        13: [27, "GPIO", "GEN2", "General Purpose I/O ()"],
        14: [None, "GND", "GND", "Ground"],
        15: [22, "GPIO", "GEN3", "General Purpose I/O ()"],
        16: [23, "GPIO", "GEN4", "General Purpose I/O ()"],
        17: [None, "PWR", "3V3", "3.3V Power"],
        18: [24, "GPIO", "GEN5", "General Purpose I/O ()"],
        19: [10, "GPIO", "MOSI", "General Purpose I/O (SPI Master OUT Slave IN)"],
        20: [None, "GND", "GND", "Ground"],
        21: [9, "GPIO", "MISO", "General Purpose I/O (SPI Master IN Slave OUT)"],
        22: [25, "GPIO", "GEN6", "General Purpose I/O ()"],
        23: [11, "GPIO", "SCLK", "General Purpose I/O (SPI Clock)"],
        24: [8, "GPIO", "CE0", "General Purpose I/O None()"],
        25: [None, "GND", "GND", "Ground"],
        26: [7, "GPIO", "CE1", "General Purpose I/O ()"],
        27: [None, "ID_EEPROM", "ID_SD", "HAT ID EEPROM"],
        28: [None, "ID_EEPROM", "ID_SC", "HAT ID EEPROM"],
        29: [5, "GPIO", "GPIO", "General Purpose I/O"],
        30: [None, "GND", "GND", "Ground"],
        31: [6, "GPIO", "GPIO", "General Purpose I/O"],
        32: [12, "GPIO", "GPIO", "General Purpose I/O"],
        33: [13, "GPIO", "GPIO", "General Purpose I/O"],
        34: [None, "GND", "GND", "Ground"],
        35: [19, "GPIO", "GPIO", "General Purpose I/O"],
        36: [16, "GPIO", "GPIO", "General Purpose I/O"],
        37: [26, "GPIO", "GPIO", "General Purpose I/O"],
        38: [20, "GPIO", "GPIO", "General Purpose I/O"],
        39: [None, "GND", "GND", "Ground"],
        40: [21, "GPIO", "GPIO", "General Purpose I/O"],
    },
}
