import json
import sys
import os

# Initialize a counter for all lines
counter = 1

# Function to convert each line to a JSON object
def line_to_json(line, json_dict):
    global counter
    parts = line.split(':', 1)
    if len(parts) == 2:
        json_dict[str(counter)] = f"{parts[0].strip()}:{parts[1].strip()}"
    else:
        json_dict[str(counter)] = line.strip()
    counter += 1  # Increment the counter

# Read the text file and convert each line
def convert_to_json(input_file, output_dir=None):
    global counter
    # Reset counter for each file conversion
    counter = 1

    # Extract filename without extension and directory
    file_dir, file_name = os.path.split(input_file)
    name_without_ext = os.path.splitext(file_name)[0]

    # Determine output file location
    if output_dir:
        output_file = os.path.join(output_dir, name_without_ext + '.json')
    else:
        output_file = os.path.join(file_dir, name_without_ext + '.json')

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    json_dict = {}
    for line in lines:
        if line.strip():
            line_to_json(line, json_dict)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_dict, file, ensure_ascii=False, indent=4)

# Check if input file and optionally output directory are provided as command-line arguments
if len(sys.argv) == 2:
    input_filename = sys.argv[1]
    convert_to_json(input_filename)
elif len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_directory = sys.argv[2]
    convert_to_json(input_filename, output_directory)
else:
    print("Usage: python convert_to_json.py input.txt [output_directory]")
