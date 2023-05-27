
from controller import RpiPin as Pin, SpiByte
from controller import GpioHandler, SerialPeripheralInterface


class Expander:
    def __init__(self):
        self._gpio = GpioHandler()
        self._spi = SerialPeripheralInterface()

        self.initialize()

    def initialize(self):
        for pin in [Pin.GPIO1_SELECT, Pin.GPIO2_SELECT, Pin.GPIO3_SELECT, Pin.GPIO4_SELECT]:
            self._gpio.init_output(pin)
        for pin in [Pin.GPIO1_SELECT, Pin.GPIO2_SELECT, Pin.GPIO3_SELECT, Pin.GPIO4_SELECT]:
            self._gpio.set(pin, 1)

        self.init_gpio(Pin.GPIO1_SELECT, SpiByte.ALL_INPUT.value, SpiByte.ALL_OUTPUT.value)
        self.init_gpio(Pin.GPIO2_SELECT, SpiByte.ALL_INPUT.value, SpiByte.ALL_INPUT.value)
        self.init_gpio(Pin.GPIO3_SELECT, SpiByte.ALL_OUTPUT.value, SpiByte.ALL_INPUT.value)
        self.init_gpio(Pin.GPIO4_SELECT, [0, 0, 1, 1, 1, 1, 1, 1], SpiByte.ALL_INPUT.value)

    def init_gpio(self, select: Pin, config_a: list[int], config_b: list[int]):
        self._spi.write(select, SpiByte.GPIO_OPCODE_WRITE.value + SpiByte.GPIO_SELECT_IOCON.value + SpiByte.ALL_OUTPUT.value)
        self._spi.write(select, SpiByte.GPIO_OPCODE_WRITE.value + SpiByte.GPIO_SELECT_DIRA.value + config_a)  # configure pins on side A
        self._spi.write(select, SpiByte.GPIO_OPCODE_WRITE.value + SpiByte.GPIO_SELECT_DIRB.value + config_b)  # configure pins on side B

    def read_gpio(self, select: int, side: str):
        spi_info = self.get_pin_and_port(select, side)
        return self._spi.read(spi_info[0], SpiByte.GPIO_OPCODE_READ.value + spi_info[1].value, 8)

    def write_gpio(self, select: int, side: str, message: list[int]) -> list[int]:
        if len(message) != 8:
            raise Exception(f"ERROR: message must be of size {8} bits but got {len(message)} bits instead")
        spi_info = self.get_pin_and_port(select, side)
        return self._spi.write(spi_info[0], SpiByte.GPIO_OPCODE_WRITE.value + spi_info[1].value + message)

    @staticmethod
    def get_pin_and_port(pin: int, port: str) -> [Pin, SpiByte]:
        if pin == 1 and port == "A":
            return [Pin.GPIO1_SELECT, SpiByte.GPIO_SELECT_PORTA]
        elif pin == 1 and port == "B":
            return [Pin.GPIO1_SELECT, SpiByte.GPIO_SELECT_PORTB]
        elif pin == 2 and port == "A":
            return [Pin.GPIO2_SELECT, SpiByte.GPIO_SELECT_PORTA]
        elif pin == 2 and port == "B":
            return [Pin.GPIO2_SELECT, SpiByte.GPIO_SELECT_PORTB]
        elif pin == 3 and port == "A":
            return [Pin.GPIO3_SELECT, SpiByte.GPIO_SELECT_PORTA]
        elif pin == 3 and port == "B":
            return [Pin.GPIO3_SELECT, SpiByte.GPIO_SELECT_PORTB]
        elif pin == 4 and port == "A":
            return [Pin.GPIO4_SELECT, SpiByte.GPIO_SELECT_PORTA]
        elif pin == 4 and port == "B":
            return [Pin.GPIO4_SELECT, SpiByte.GPIO_SELECT_PORTB]
        else:
            raise Exception(f"ERROR: invalid select '{pin}' or side '{port}' for GPIO Expander.")
