# Define variables
PYTHON = python
SRC = gatorDelivery.py
INPUT_FILE = test1.txt

# Extract the base name of the input file
BASE_FILENAME := $(basename $(INPUT_FILE))
# Define the output file name
OUTPUT_FILE := $(BASE_FILENAME)_output_file.txt

# Default target
all: $(SRC)

# Rule to run the program
run: $(SRC)
	$(PYTHON) $(SRC) $(INPUT_FILE)

# Clean rule to remove generated files
clean:
	rm -f *_output_file.txt

# Phony targets
.PHONY: all run clean