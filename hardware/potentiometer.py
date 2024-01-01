from common import integer_to_binary_string
from hardware import Pin, SpiDevice


class MCP42XXX(SpiDevice):
    """
    MicroChip Serial Interface (SPI) Digital Potentiometer device implementation for Raspberry Pi.

    SPI Protocol:
     * Data out of the device (MISO) will always match the last command it was sent (shift register configuration).
     * Data is clocked IN  (MOSI) on the 'rising'  edge of the clock signal.
     * Data is clocked OUT (MISO) on the 'falling' edge of the clock signal.
     * All messages MUST have exactly 16 clock signals (rising edges); otherwise operation will be aborted by device.

     [ ======== COMMAND BYTE ========= ] [ ============ DATA BYTE ============ ]
     [X] [X] [C1] [C0] [X] [X] [P1] [P0] [D7] [D6] [D5] [D4] [D3] [D2] [D1] [D0]

     * C1/C0 are the "command selection bits", and correspond to the following values:
        00 & 11 = No Command (None)
        01 = Write
        10 = Shutdown

     * P1/P0 are the "potentiometer selection bits", and correspond to the following values:
        00 = Neither (None)
        01 = Potentiometer 0
        10 = Potentiometer 1
        11 = Both Potentiometers
    """

    def __init__(self, name: str, reset: Pin = None, shutdown: Pin = None) -> None:
        super().__init__(name)

        # Optionally, set rest pin (if `reset` provided)
        if reset:
            self.set_reset_pin(reset)

        # Optionally, set shutdown pin (if `reset` provided)
        if shutdown:
            self.set_shutdown_pin(shutdown)

    def write_pot(self, resistance: int, pot_select: int) -> None:
        """
        Write a resistance value to the digital potentiometer. Takes 2 positional argument:

        :param resistance: Resistance value to write to the digital potentiometer (in Ohms).
        :param pot_select: Selects which Potentiometer to write to (must be either 0 or 1).
        """
        # Validate
        if resistance < 0 or resistance > (2 ** 8):
            raise Exception(f"Invalid resistance value '{resistance}' (must be between 0 and {2 ** 8} Ohms).")
        if pot_select != 0 and pot_select != 1:
            raise Exception(f"Invalid potentiometer selection '{pot_select}' (must be either 0 or 1).")

        self._logger.info(f"{self.name}: Writing '{resistance}' to potentiometer {pot_select}")

        # Write to device
        cmd_select_bits = "01"  # For 'write' operation
        pot_select_bits = "10" if pot_select == 1 else "01"  # Assumes pot_select equals either 0 or 1
        data_bits = integer_to_binary_string(resistance)
        self.write(f"00{cmd_select_bits}00{pot_select_bits}{data_bits}")
