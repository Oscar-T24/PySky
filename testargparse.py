import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Print the value of a command line argument')

# Add an argument to the parser
parser.add_argument('-value', help='the value to be printed')

# Parse the command line arguments
args = parser.parse_args()

# Print the value of the argument
print(args.value)