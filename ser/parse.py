#!/usr/bin/python3
def read_and_append_binary(input_file, output_file):
    try:
        # Open the input file and read the lines
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        # Open the output file in append binary mode
        with open(output_file, 'ab') as outfile:
            for line in lines:
                # Convert the string representation of bytes into actual bytes
                byte_line = eval(line.strip())  # `eval` safely interprets the byte string
                outfile.write(byte_line)        # Append the binary data to the output file
            print(f"Data successfully appended to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

# Main execution
if __name__ == "__main__":
    input_file = "data"        # File containing the lines with byte strings
    output_file = "output.bin" # File to which the binary data will be appended

    read_and_append_binary(input_file, output_file)

