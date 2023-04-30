from enum import Enum

from controller import int_to_binary

try:
    # TODO: the old controller used this library
    import RPi.GPIO as GPIO
    # TODO: this library supports SPI, maybe also consider pigpio which supports SPI, I2C, and UART
    # import gpiozero as gpio
except ModuleNotFoundError:
    print("ERROR: Could not import RPi.GPIO")


class GpioPin(Enum):
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


class GPIOHandler:
    def __init__(self):
        print("Initializing GPIO Handler...")

    def init_pot(self):
        value = 1.0
        message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        self.write_spi(GpioPin.POT_SELECT, message)

    def init_xpndr(self):
        self.write_spi(GpioPin.GPIO1_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        self.write_spi(GpioPin.GPIO1_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRB

        self.write_gpio(GpioPin.GPIO1_SELECT, [0, 0, 0, 0, 0, 0, 0, 0], "B")

        self.write_spi(GpioPin.GPIO2_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        self.write_spi(GpioPin.GPIO2_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB

        self.write_spi(GpioPin.GPIO3_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))  # write IODIRA
        self.write_spi(GpioPin.GPIO3_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRB

        self.write_spi(GpioPin.GPIO4_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1))  # write IODIRA
        self.write_spi(GpioPin.GPIO4_SELECT, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1))

    @staticmethod
    def init_gpio():
        # GPIO.init()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(GpioPin.CLK, GPIO.OUT)
        GPIO.setup(GpioPin.MOSI, GPIO.OUT)
        GPIO.setup(GpioPin.MISO, GPIO.IN)
        GPIO.setup(GpioPin.POT_SELECT, GPIO.OUT)
        GPIO.setup(GpioPin.ADC_SELECT, GPIO.OUT)
        GPIO.setup(GpioPin.POWER_DOWN, GPIO.OUT)
        GPIO.setup(GpioPin.GPIO1_SELECT, GPIO.OUT)
        GPIO.setup(GpioPin.GPIO2_SELECT, GPIO.OUT)
        GPIO.setup(GpioPin.GPIO3_SELECT, GPIO.OUT)
        GPIO.setup(GpioPin.GPIO4_SELECT, GPIO.OUT)
        GPIO.setup(GpioPin.ACCESSORY_POWER, GPIO.IN)

        GPIO.output(GpioPin.CLK, 0)
        GPIO.output(GpioPin.MOSI, 0)
        GPIO.output(GpioPin.POT_SELECT, 1)
        GPIO.output(GpioPin.ADC_SELECT, 1)
        GPIO.output(GpioPin.GPIO1_SELECT, 1)
        GPIO.output(GpioPin.GPIO2_SELECT, 1)
        GPIO.output(GpioPin.GPIO3_SELECT, 1)
        GPIO.output(GpioPin.GPIO4_SELECT, 1)
        GPIO.output(GpioPin.POWER_DOWN, 0)

    def write_gpio(self, slave, byte, gpio: str):
        # TODO: should probably make some sort of GPIO class abstraction...
        if gpio == "A":
            message = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0] + byte
            self.write_spi(slave, message)  # write GPIO A
        elif gpio == "B":
            message = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1] + byte
            self.write_spi(slave, message)  # write GPIO B
        else:
            raise Exception(f"Invalid GPIO '{gpio}'")

    def read_gpio(self, slave, gpio: str):
        # TODO: should probably make some sort of GPIO class abstraction...
        if gpio == "A":
            message = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
            return self.read_gpio_spi(slave, message)  # write GPIO A
        elif gpio == "B":
            message = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
            return self.read_gpio_spi(slave, message)  # write GPIO B
        else:
            raise Exception(f"Invalid GPIO '{gpio}'")

    def set_pot(self, value):
        value = max(0., min(1., 1. - value))
        message = [0, 0, 0, 1, 0, 0, 0, 1] + int_to_binary(int(value * 255))
        self.write_spi(GpioPin.POT_SELECT, message)

    @staticmethod
    def write_spi(slave, message):
        GPIO.output(slave, 0)
        # time.sleep(0.005)
        for entry in message:
            GPIO.output(GpioPin.MOSI, entry)
            GPIO.output(GpioPin.CLK, 1)
            # time.sleep(0.005)
            GPIO.output(GpioPin.CLK, 0)
            # time.sleep(0.005)
        GPIO.output(GpioPin.MOSI, 0)
        GPIO.output(slave, 1)
        # time.sleep(0.005)

    @staticmethod
    def read_adc(channel) -> float:
        read = []
        message = [0, 1, 1]
        bin_channel = int_to_binary(channel)[-3:]
        message += bin_channel
        GPIO.output(GpioPin.ADC_SELECT, 0)
        message = (0, 1, 1, 0, 0, 1)

        for entry in message:
            GPIO.output(GpioPin.MOSI, entry)
            GPIO.output(GpioPin.CLK, 1)
            GPIO.output(GpioPin.CLK, 0)

        for _ in range(12):
            GPIO.output(GpioPin.CLK, 1)
            GPIO.output(GpioPin.CLK, 0)
            read.append(GPIO.input(GpioPin.MISO))

        GPIO.output(GpioPin.ADC_SELECT, 1)
        return binary_to_decimal(read)

    @staticmethod
    def read_gpio_spi(slave, message: tuple):
        GPIO.output(slave, 0)
        # time.sleep(0.005)
        read = []
        for entry in message:
            GPIO.output(GpioPin.MOSI, entry)
            GPIO.output(GpioPin.CLK, 1)
            # time.sleep(0.005)
            GPIO.output(GpioPin.CLK, 0)
            # time.sleep(0.005)
        for entry in range(8):
            GPIO.output(GpioPin.CLK, 1)
            # time.sleep(0.005)
            read.append(GPIO.input(GpioPin.MISO))
            GPIO.output(GpioPin.CLK, 0)
            # time.sleep(0.005)
        GPIO.output(slave, 1)
        # time.sleep(0.005)
        return read


class GPIOHandlerDummy:
    def __init__(self):
        print("WARNING: This is a dummy GPIOHandler class for testing")

    def init_pot(self):
        pass

    def init_xpndr(self):
        pass

    @staticmethod
    def init_gpio():
        pass

    def write_gpio(self, slave, byte, gpio: str):
        pass

    def read_gpio(self, slave, gpio: str):
        pass

    def set_pot(self, value):
        pass

    @staticmethod
    def write_spi(slave, message):
        pass

    @staticmethod
    def read_adc(channel) -> float:
        pass

    @staticmethod
    def read_gpio_spi(slave, message: tuple):
        pass
