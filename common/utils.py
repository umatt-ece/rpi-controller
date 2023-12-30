"""
This file contains a collection of utility functions common to all modules of this project.
"""


def validate_binary_string(binary_string: str, identifier: str = "") -> str:
    """
    Validate that the given string a representation of a binary number, containing only 0's and 1's. Takes 1 positional
    argument, and one optional keyword argument:

    :param binary_string: The string to validate (should contain only 0's and 1's).
    :param identifier: Optional string description of the `binary_string` use (for robust logging).
    """
    # Validate the binary string
    for bit in binary_string:
        if bit != "0" and bit != "1":
            raise Exception(
                f"{identifier}: '{binary_string}' is not a valid binary string ({bit} must be either '0' or '1')")
    # Return the string if valid
    return binary_string


def swap_string_endian(byte_message: str) -> str:
    return byte_message[::-1]


def integer_to_binary_string(integer: int) -> str:
    return bin(integer)[2:]


def binary_string_to_integer(binary_string: str) -> int:
    return int(binary_string, 2)
