"""
Package: Common
Purpose: This package contains code used by all modules of the project, helping to reduce the amount of repeated
         code fragments.
"""
from .utils import validate_binary_string, swap_string_endian, integer_to_binary_string, binary_string_to_integer
from .dependency_handler import get_data_store, get_client_manager, get_raspberry_pi
