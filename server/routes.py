import logging
from fastapi import APIRouter, Body
from fastapi_utils.cbv import cbv

from hardware import RaspberryPi

router = APIRouter()


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


@cbv(router)
class SystemRoutes:
    def __init__(self):
        self._logger = logging.getLogger("server")

        self._data_store = inject_data_store()
        self._rpi = inject_raspberry_pi(RaspberryPi.RPI4B)

    @router.post("/api/test", tags=["Testing"])
    async def test_route(self, value: dict = Body(...)) -> None:
        """
        This is just a "hello_world"-style testing route. It logs the contents of the _post_ message body.

        ***This route is intended for testing, and should not be called by production code.***
        """
        self._logger.info(f"Route '/api/test' was called with value: {value}")

    @router.post("/api/write-pin", tags=["Testing"])
    async def write_pin_route(self, gpio: int, port: str, pin: int, value: bool) -> None:
        """
        Directly calls `write_pin` for a device with name starting with "gpio_". The assumption is made that all device
        names that start with _gpio_ are of type MCP23S17 and have a class function `write_pin`. Additionally, **port**
        (either "A" or "B"), **pin** (between 0-7), and **value** (state to write) are required parameters.

        ***This route is intended for testing, and should not be called by production code.***
        """
        try:
            self._rpi.devices[f"gpio_{gpio}"].write_pin(port=port, pin=pin, value=value)
        except Exception as e:
            self._logger.error(f"Exception occurred during handling of '/api/write-pin'...")
            self._logger.exception(e)

    @router.get("/api/read-pin", tags=["Testing"])
    async def read_pin_route(self, gpio: int, port: str, pin: int) -> bool:
        """
        Directly calls `read_pin` for a device with name starting with "gpio_". The assumption is made that all device
        names that start with _gpio_ are of type MCP23S17 and have a class function `read_pin`. Additionally, **port**
        (either "A" or "B"), **pin** (between 0-7), and **value** (state to write) are required parameters.

        ***This route is intended for testing, and should not be called by production code.***
        """
        try:
            return self._rpi.devices[f"gpio_{gpio}"].read_pin(port=port, pin=pin)
        except Exception as e:
            self._logger.error(f"Exception occurred during handling of '/api/read-pin'...")
            self._logger.exception(e)

    @router.get("/api/read-analog", tags=["Testing"])
    async def read_analog_route(self, adc: int, channel: int) -> int:
        """
        Directly calls `read_analog` for a device with name starting with "adc_". The assumption is made that all
        device names that start with _adc_ are of type MCP3208 and have a class function `read_analog`. Additionally,
        **channel** (between 0-7 if configured in single-ended mode of 0-3 if configured in differential mode) are
        required parameters.

        ***This route is intended for testing, and should not be called by production code.***
        """
        try:
            return self._rpi.devices[f"adc_{adc}"].read_analog(channel=channel)
        except Exception as e:
            self._logger.error(f"Exception occurred during handling of '/api/read-analog'...")
            self._logger.exception(e)

    @router.post("/api/write-pot", tags=["Testing"])
    async def write_pot_route(self, pot: int, resistance: int, select: int) -> int:
        """
        Directly calls `write_pot` for a device with name starting with "pot_". The assumption is made that all
        device names that start with _pot_ are of type MCP42XXX and have a class function `write_pot`. Additionally,
        **resistance** (integer value in Ohms) and **select** (either 0 or 1) are required parameters.

        ***This route is intended for testing, and should not be called by production code.***
        """
        try:
            self._rpi.devices[f"pot_{pot}"].write_pot(resistance=resistance, pot_select=select)
        except Exception as e:
            self._logger.error(f"Exception occurred during handling of '/api/write-pot'...")
            self._logger.exception(e)
