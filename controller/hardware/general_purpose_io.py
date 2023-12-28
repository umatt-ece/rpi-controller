from enum import Enum

from .interfaces import SpiDevice


class MCP23S17Register(Enum):
    IODIRA = "00000000"
    IODIRB = "00010000"
    GPIOA = "00001001"
    GPIOB = "00011001"


class MCP23S17(SpiDevice):
    """
    Serial Interface (SPI) 16-bit I/O Expander
    """
    _config = {}
    _pin_state = {
        "A": "00000000",
        "B": "00000000",
    }

    def __init__(self, name: str, address: str, config: dict = None) -> None:
        super().__init__(name, f"0100{address}")

        # Optionally, configure the device on initialization
        if config:
            self.configure(config)

    def configure(self, config: dict) -> None:
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

        self.write(f"{MCP23S17Register.IODIRA.value}{message_byte_a}")  # Configure Port A
        self.write(f"{MCP23S17Register.IODIRB.value}{message_byte_b}")  # Configure Port B

    def write_io(self, port: str, pin: int, value: bool) -> None:
        self._logger.info(f"Writing '{'1' if value else '0'}' to {self.name} pin {port}{pin}")

        if pin < 0 or pin > 7:
            self._logger.error(f"'{pin}' is not a valid pin (must be between 0 and 7)")
            raise Exception(f"Invalid pin number {pin}")
        if port == "A":
            register_byte = MCP23S17Register.GPIOA.value
            message_byte = f"{self._pin_state['A'][:pin]}{'1' if value else '0'}{self._pin_state['A'][pin + 1:]}"
            self._pin_state["A"] = message_byte  # update pin states
        elif port == "B":
            register_byte = MCP23S17Register.GPIOB.value
            message_byte = f"{self._pin_state['B'][:pin]}{'1' if value else '0'}{self._pin_state['B'][pin + 1:]}"
            self._pin_state["A"] = message_byte  # update pin states
        else:
            self._logger.error(f"'{port}' is not a valid port (must be 'A' or 'B')")
            raise Exception(f"Invalid port value {port}")

        self.write(f"{register_byte}{message_byte}")

    def read_io(self, port: str, pin: int) -> bool:
        self._logger.info(f"Reading pin {port}{pin} of {self.name}")

        if pin < 0 or pin > 7:
            self._logger.error(f"'{pin}' is not a valid pin (must be between 0 and 7)")
            raise Exception(f"Invalid pin number {pin}")
        if port == "A":
            register_byte = MCP23S17Register.GPIOA.value
        elif port == "B":
            register_byte = MCP23S17Register.GPIOB.value
        else:
            self._logger.error(f"'{port}' is not a valid port (must be 'A' or 'B')")
            raise Exception(f"Invalid port value {port}")

        value = self.read(1, register_byte)

        self._logger.info(f"{self.name}: pin {port}{pin} = '{value[pin] == '1'}'")
        return value[pin] == "1"  # return True if "1" or False if "0"

    def _parse_value(self, value: str) -> bool:
        if value == "00000000":
            return False
        elif value == "00000001":
            return True
        else:
            self._logger.error(f"Invalid value '{value}'")


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
