import logging

from hardware import RaspberryPi, RPiModel, SpiDevice


def main():
    try:
        gpio = SpiDevice("gpio", "0101001")

        rpi = RaspberryPi(RPiModel.RPI4B)
        rpi.print_pinout()

        rpi.configure_spi("GPIO11", "GPIO10", "GPIO9")
        rpi.add_spi_device(gpio, "GPIO6")

        print(rpi.list_devices)

        rpi.devices['gpio'].write("0000111100110011")
        rpi.devices['gpio'].read(2)

    except Exception as e:
        # TODO: log exceptions first...
        print("Oh no, something went wrong...")


if __name__ == "__main__":
    main()
