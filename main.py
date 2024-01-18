import logging
import threading
import time

from hardware import MCP23S17, RaspberryPi
from logic import EVTStateMachine
from server import start_vue_server

INTERVAL = 1  # seconds
stop_all_threads = False

_logger = logging.getLogger("controller")

demo_config = {
    "name": "demo",
    "gpio": [
        {
            "name": "gpio_0",
            "address": "000",
            "select": "GPIO6",
            "reset": "GPIO5",
            "port_config": {
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
            },
        }, {
            "name": "gpio_1",
            "address": "001",
            "select": "GPIO6",
            "reset": "GPIO5",
            "port_config": {
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
            },
        }, {
            "name": "gpio_2",
            "address": "010",
            "select": "GPIO6",
            "reset": "GPIO5",
            "port_config": {
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
            },
        }, {
            "name": "gpio_3",
            "address": "011",
            "select": "GPIO6",
            "reset": "GPIO5",
            "port_config": {
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
            },
        }
    ]

}


def inject_data_store(logger: logging.Logger = None):
    """
    In order to avoid circular imports during initialization, the get_data_store function must be imported later
    and called within this function.
    """
    from common.dependency_handler import get_data_store
    return get_data_store(logger=logger)


def inject_raspberry_pi(model: str, logger: logging.Logger = None):
    """
    In order to avoid circular imports during initialization, the get_raspberry_pi function must be imported later
    and called within this function.
    """
    from common.dependency_handler import get_raspberry_pi
    return get_raspberry_pi(model=model, logger=logger)


def stop_thread() -> bool:
    return stop_all_threads


def main():
    try:  # Setup & Initialization

        _logger.info("Initializing RPi-Controller Software...")

        config = demo_config
        _logger.info(f"Using Config: {config['name']}")

        # Configure Raspberry Pi
        rpi = inject_raspberry_pi(RaspberryPi.RPI4B)
        rpi.configure_spi(clock="GPIO11", mosi="GPIO10", miso="GPIO9")
        rpi.pinout()  # print pinout for reference

        # Configure GPIO devices
        gpio_devices = []
        for gpio_config in config["gpio"]:
            gpio_device = MCP23S17(gpio_config["name"], address=gpio_config["address"])
            gpio_devices.append(gpio_device)

            rpi.add_spi_device(device=gpio_device, select=gpio_config["select"], reset=gpio_config["reset"])
            rpi.devices[gpio_config["name"]].configure(gpio_config["port_config"], haen=True)

        # adc_0 = MCP3208("adc_0", mode=MCP3208.SINGLE)
        # pot_0 = MCP42XXX("pot_0")

        # rpi.add_spi_device(device=adc_0, select="GPIO6")
        # rpi.add_spi_device(device=pot_0, select="GPIO6", reset="GPIO5", shutdown="GPIO13")

        # Initialize Date Store
        data_store = inject_data_store()

        # Initialize Demo State Machine
        demo_state_machine = DemoStateMachine(name="demo", rpi=rpi, datastore=data_store)
        demo_thread = threading.Thread(target=demo_state_machine.run, args=[stop_thread])
        demo_thread.start()

        # Initialize Drive State Machines
        drive_state_machine = EVTStateMachine(name="evt", rpi=rpi, datastore=data_store)
        drive_thread = threading.Thread(target=drive_state_machine.run, args=[stop_thread])
        drive_thread.start()

        # Start Vue API web-server
        vue_thread = threading.Thread(target=start_vue_server)
        vue_thread.start()

        while True:  # Main Program Loop

            # Example Usage of RPi device functions
            # rpi.devices["gpio_0"].write_pin(port="A", pin=7, value=True)
            # rpi.devices["gpio_0"].read_pin(port="B", pin=0)
            # rpi.devices["adc_0"].read_analog(channel=0)
            # rpi.devices["pot_0"].write_pot(resistance=100, pot_select=0)

            # Delay processor execution (not necessary to run as fast as possible)
            time.sleep(INTERVAL)

    except Exception as e:
        # Attempt to stop all threads gracefully
        global stop_all_threads
        stop_all_threads = True
        # Log the exception
        _logger.exception(e)
        # Throw it back so we can still crash
        raise e


if __name__ == "__main__":
    main()
