"""
Package: Hardware
Purpose: This package contains driver code and low-level hardware abstractions for working with peripherals and other
         physical hardware.
"""
from .test.dummy_gpio import RPiGPIO

from .peripherals import Pin
from .interfaces import SerialPeripheralInterface, SpiDevice
from .raspberry_pi import RaspberryPi, RPiModel
from .general_purpose_io import MCP23S17
from .analog_digital_converter import MCP3208
from .potentiometer import MCP42XXX
