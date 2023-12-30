from unittest.mock import Mock, call

from hardware import Pin, SerialPeripheralInterface, SpiDevice


class TestSerialPeripheralInterface:

    @staticmethod
    def setup() -> SerialPeripheralInterface:
        return SerialPeripheralInterface(select=Mock(), clock=Mock(), mosi=Mock(), miso=Mock(), logger=Mock())

    def test_write(self):
        # Arrange
        sut = self.setup()
        # Act
        sut.write("01")
        # Assert\
        assert sut._select.write.call_count == 2
        sut._select.write.assert_has_calls([call(0), call(1)])
        assert sut._clock.write.call_count == 4
        sut._clock.write.assert_has_calls([call(1), call(0), call(1), call(0)])
        assert sut._mosi.write.call_count == 3
        sut._mosi.write.assert_has_calls([call(0), call(1), call(0)])
        assert sut._miso.read.call_count == 0

    def test_read(self):
        # Arrange
        sut = self.setup()
        # Act
        sut.read(1)
        # Assert
        assert sut._select.write.call_count == 2
        sut._select.write.assert_has_calls([call(0), call(1)])
        assert sut._clock.write.call_count == 2
        sut._clock.write.assert_has_calls([call(1), call(0)])
        assert sut._mosi.write.call_count == 1
        sut._mosi.write.assert_has_calls([call(0)])
        assert sut._miso.read.call_count == 1

    def test_read_with_message(self):
        # Arrange
        sut = self.setup()
        # Act
        sut.read(2, message="01")
        # Assert
        assert sut._select.write.call_count == 2
        sut._select.write.assert_has_calls([call(0), call(1)])
        assert sut._clock.write.call_count == 8
        sut._clock.write.assert_has_calls([call(1), call(0), call(1), call(0), call(1), call(0), call(1), call(0)])
        assert sut._mosi.write.call_count == 3
        sut._mosi.write.assert_has_calls([call(0), call(1), call(0)])
        assert sut._miso.read.call_count == 2


class TestSpiDevice:

    def test_set_address(self):
        # Arrange
        sut = SpiDevice("Test")
        # Act
        sut.set_address("001")
        # Assert
        assert sut.address == "001"

    def test_set_interface(self):
        # Arrange
        sut = SpiDevice("Test")
        test_interface = SerialPeripheralInterface(Mock(), Mock(), Mock(), Mock())
        # Act
        sut.set_interface(test_interface)
        # Assert
        assert sut._interface == test_interface

    def test_set_reset_pin(self):
        # Arrange
        sut = SpiDevice("Test")
        test_pin = Pin(0)
        # Act
        sut.set_reset_pin(test_pin)
        # Assert
        assert sut._reset == test_pin

    def test_write(self):
        # Arrange
        sut = SpiDevice("Test")
        test_interface = Mock()
        sut.set_interface(test_interface)
        # Act
        sut.write("0101")
        # Assert
        test_interface.write.assert_called_with("0101")

    def test_write_no_interface(self):
        # Arrange
        sut = SpiDevice("Test", logger=Mock())
        # Act
        sut.write("0101")
        # Assert
        sut._logger.error.assert_called()

    def test_read(self):
        # Arrange
        sut = SpiDevice("Test")
        test_interface = Mock()
        sut.set_interface(test_interface)
        # Act
        sut.read(3)
        sut.read(2, "101")
        # Assert
        test_interface.read.assert_has_calls([call(3, ""), call(2, "101")])

    def test_read_no_interface(self):
        # Arrange
        sut = SpiDevice("Test", logger=Mock())
        # Act
        sut.read(4, "01")
        # Assert
        sut._logger.error.assert_called()
