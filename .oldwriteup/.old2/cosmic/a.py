def show_bit_changes(start_num, num1, num2):
  
  # Convert both numbers to binary
  bin1 = bin(num1)[2:].zfill(64)
  bin2 = bin(num2)[2:].zfill(64)

  # Initialize a list to store the positions of changes
  changed_bits = []

  # Iterate through the bits and compare
  for i in range(64):
    if bin1[i] != bin2[i]:
      changed_bits.append(start_num + i)

  # Print the results
  return changed_bits


