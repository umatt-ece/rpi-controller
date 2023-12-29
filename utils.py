

# def int_to_binary(integer: int) -> bin:
#     binary_text = bin(integer)[2:]
#     binary = []
#     for ii in range(8 - len(binary_text)):
#         binary.append(0)
#     for ii in range(len(binary_text)):
#         binary.append(int(binary_text[ii]))
#     return binary
#
#
# def binary_to_decimal(message: list) -> float:
#     number = 0
#     for ii in range(len(message)):
#         number += message[len(message) - 1 - ii] * (2 ** ii)
#     return number
