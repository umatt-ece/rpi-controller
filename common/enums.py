from enum import Enum


class RpiPin(Enum):
    CLK = 23  # clock for Serial Peripheral Interface (communication protocol) I think...
    MOSI = 10  # 'master out slave in' for SPI
    MISO = 25  # 'master in slave out' for SPI
    POT_SELECT = 8  # Potentiometer (???)
    ADC_SELECT = 5  # Analog Digital Converter
    POWER_DOWN = 12  # Tractor Power
    GPIO1_SELECT = 24
    GPIO2_SELECT = 9
    GPIO3_SELECT = 11
    GPIO4_SELECT = 6
    ACCESSORY_POWER = 16

    TEST_PIN = 17
