import logging
import time

import __init__
from hardware import RPiModel, RaspberryPi, MCP23S17, MCP3208, MCP42XXX


INTERVAL = 1  # seconds


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
        0: "input",
        1: "input",
        2: "input",
        3: "input",
        4: "input",
        5: "input",
        6: "input",
        7: "input",
    }
}


def main():
    try:  # Setup & Initialization

        # Configure devices
        gpio_0 = MCP23S17("gpio_0", address="000")
        gpio_1 = MCP23S17("gpio_1", address="001")
        gpio_2 = MCP23S17("gpio_2", address="010")
        gpio_3 = MCP23S17("gpio_3", address="011")
        adc = MCP3208("adc", mode=MCP3208.SINGLE)
        pot = MCP42XXX("pot")

        # Configure Raspberry Pi
        rpi = RaspberryPi(RPiModel.RPI4B)
        rpi.configure_spi(clock="GPIO11", mosi="GPIO10", miso="GPIO9")
        rpi.pinout()  # print pinout for reference

        # Add devices to Raspberry Pi
        rpi.add_spi_device(device=gpio_0, select="GPIO6", reset="GPIO5")
        rpi.add_spi_device(device=gpio_1, select="GPIO6", reset="GPIO5")
        rpi.add_spi_device(device=gpio_2, select="GPIO6", reset="GPIO5")
        rpi.add_spi_device(device=gpio_3, select="GPIO6", reset="GPIO5")
        rpi.add_spi_device(device=adc, select="GPIO6")
        rpi.add_spi_device(device=pot, select="GPIO6", reset="GPIO5", shutdown="GPIO13")

        # Configure GPIO devices for Hardware Addressing (HAEN)
        rpi.devices["gpio_0"].configure(sample_gpio_config, haen=True)
        rpi.devices["gpio_1"].configure(sample_gpio_config, haen=True)
        rpi.devices["gpio_2"].configure(sample_gpio_config, haen=True)
        rpi.devices["gpio_3"].configure(sample_gpio_config, haen=True)

        while True:  # Main Program Loop

            # Example Usage of RPi device functions
            rpi.devices["gpio_0"].write_pin(port="A", pin=7, value=True)
            rpi.devices["gpio_0"].read_pin(port="B", pin=0)
            rpi.devices["adc"].read_analog(channel=0)
            rpi.devices["pot"].write_pot(resistance=100, pot_select=0)

            # Delay processor execution (not necessary to run as fast as possible)
            time.sleep(INTERVAL)

    except Exception as e:
        # TODO: log exceptions first...
        logger.exception(e)
        logger.error("Oh no, something went wrong...")


if __name__ == "__main__":
    main()
