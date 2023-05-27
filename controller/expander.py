
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

        # GPIO1
        # writeSPI(p_GPIO1Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        # writeSPI(p_GPIO1Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRB
        #
        # writeGPIOB(p_GPIO1Select, [0, 0, 0, 0, 0, 0, 0, 0])
        #
        # writeSPI(p_GPIO2Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        # writeSPI(p_GPIO2Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB
        #
        # writeSPI(p_GPIO3Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRA
        # writeSPI(p_GPIO3Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB
        #
        # writeSPI(p_GPIO4Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        # writeSPI(p_GPIO4Select, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1))
        pass

    def read_gpio(self, select: int, side: str):
        spi_info = self.get_pin_and_port(select, side)
        return self._spi.read(spi_info[0], spi_info[1], 8)

    def write_gpio(self, select: int, side: str, message: list) -> list[int]:
        if len(message) != 8:
            raise Exception(f"ERROR: message must be of size {8} bits but got {len(message)} bits instead")
        spi_info = self.get_pin_and_port(select, side)
        return self._spi.write(spi_info[0], SpiByte.READ.value + spi_info[1] + message)

    @staticmethod
    def get_pin_and_port(pin: int, port: str) -> [Pin, SpiByte]:
        if pin == 1 and port == "A":
            return [Pin.GPIO1_SELECT, SpiByte.FFFF]
        elif pin == 1 and port == "A":
            return [Pin.GPIO1_SELECT, SpiByte.FFFF]
        elif pin == 2 and port == "A":
            return [Pin.GPIO2_SELECT, SpiByte.FFFF]
        elif pin == 2 and port == "A":
            return [Pin.GPIO2_SELECT, SpiByte.FFFF]
        elif pin == 3 and port == "A":
            return [Pin.GPIO3_SELECT, SpiByte.FFFF]
        elif pin == 3 and port == "A":
            return [Pin.GPIO3_SELECT, SpiByte.FFFF]
        elif pin == 4 and port == "A":
            return [Pin.GPIO4_SELECT, SpiByte.FFFF]
        elif pin == 4 and port == "A":
            return [Pin.GPIO4_SELECT, SpiByte.FFFF]
        else:
            raise Exception(f"ERROR: invalid select '{pin}' or side '{port}' for GPIO Expander.")
