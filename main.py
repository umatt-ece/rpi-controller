import logging
import time

import __init__

from hardware import RPiModel, RaspberryPi, MCP23S17

logger = logging.getLogger("controller")

sample_gpio_config = {
    "PORTA": {
        0: "output",
        1: "output",
        2: "output",
        3: "output",
        4: "output",
        5: "output",
        6: "output",
        7: "output",
    },
    "PORTB": {
        0: "output",
        1: "output",
        2: "output",
        3: "output",
        4: "output",
        5: "output",
        6: "output",
        7: "output",
    }
}


def main():
    try:
        gpio_0 = MCP23S17("gpio_0", "000")
        gpio_1 = MCP23S17("gpio_1", "001")
        gpio_2 = MCP23S17("gpio_2", "010")
        gpio_3 = MCP23S17("gpio_3", "011")

        rpi = RaspberryPi(RPiModel.RPI4B)
        rpi.pinout()

        rpi.configure_spi(clock="GPIO11", mosi="GPIO10", miso="GPIO9")
        rpi.add_spi_device(device=gpio_0, select="GPIO6")

        rpi.devices["gpio_0"].configure(sample_gpio_config)

        rpi.devices["gpio_0"].write_pin(port="B", pin=7, value=True)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=0)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=1)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=2)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=3)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=4)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=5)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=6)
        # rpi.devices["gpio_0"].read_pin(port="B", pin=7)

    except Exception as e:
        # TODO: log exceptions first...
        logger.exception(e)
        logger.error("Oh no, something went wrong...")


if __name__ == "__main__":
    main()
