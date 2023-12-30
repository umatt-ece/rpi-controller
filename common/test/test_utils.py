import pytest
import unittest

from common import validate_binary_string


# Parameter Lists
test_validate_binary_string_parameters = (
    ("0000", True),
    ("1111", True),
    ("0101", True),
    ("0b1", False),
    ("abc", False),
    ("0 1", False),
)


@pytest.mark.parametrize("binary_string, result", test_validate_binary_string_parameters)
class TestUtilsValidateBinaryString:

    @staticmethod
    def assert_raises(exception, function: callable, *args, **kwargs):
        """
        This function allows the `unittest.TestCase.assertRaises()` function to be called. Parent class cannot inherent
        from `unittest.TestCase` due to parameterization, so this is the work-around to get both functionality.
        """
        test_case = unittest.TestCase()
        test_case.assertRaises(exception, function, *args, **kwargs)

    def test_validate_binary_string(self, binary_string: str, result: bool):
        # Arrange
        if result:
            # Act / Assert
            assert validate_binary_string(binary_string) == binary_string
        else:
            # Act / Assert
            self.assert_raises(Exception, validate_binary_string, binary_string)
