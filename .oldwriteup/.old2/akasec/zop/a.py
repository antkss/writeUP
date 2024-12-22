#!/bin/python3

import base64

def hex_to_base64(hex_str):
  """Converts a hexadecimal string to base64."""
  # Remove the "0x" prefix if present
  hex_str = hex_str[2:] if hex_str.startswith("0x") else hex_str

  # Convert hexadecimal to bytes
  byte_data = bytes.fromhex(hex_str)

  # Encode bytes to base64
  base64_str = base64.b64encode(byte_data).decode('ascii')

  return base64_str

# hex_number = "0x4034b50f0f0f1f1f1f2f3f4f5f6f7f8f9f1f1f1f0f0f1f1f2f2f3f3f4f4ffff"
# if len(hex_number[2:]) % 2 != 0:  # Check if odd number of digits
#     hex_number = "0x0" + hex_number[2:]  # Add a leading zero
def reverse_bytes(hex_str):
  """Reverses the byte order in a hexadecimal string."""
  hex_str = hex_str[2:]  # Remove the "0x" prefix
  byte_list = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
  reversed_bytes = byte_list[::-1]
  return '0x' + ''.join(reversed_bytes)

hex_number = input("input hex str: ")
reversed_hex = reverse_bytes(hex_number)
if len(reversed_hex[2:]) % 2 != 0:  # Check if odd number of digits
    print("can do anything if odd")
    exit(1)
    # reversed_hex = "0x0" + reversed_hex[2:]  # Add a leading zero
base64_value = hex_to_base64(reversed_hex)
print(f"Base64: {base64_value}")
print(f"Original: {hex_number}")
print(f"Reversed: {reversed_hex}")
