from controller.hardware.rpi import RaspberryPi, pinout_mapping


def test_rpi_print_pinout():
    for mapping in pinout_mapping:
        # Arrange
        sut = RaspberryPi(mapping)
        # Act
        sut.print_pinout()
        # Assert
        assert True

