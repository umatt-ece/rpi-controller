from hardware import Pin, RPiGPIO


class TestPeripherals:

    def test_set_direction(self):
        # Arrange
        sut_0 = Pin(0)
        sut_1 = Pin(0)
        # Act
        sut_0.set_direction(RPiGPIO.IN)
        sut_1.set_direction(RPiGPIO.OUT)
        # Assert
        assert sut_0.direction == RPiGPIO.IN
        assert sut_1.direction == RPiGPIO.OUT
