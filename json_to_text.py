import json
import sys
import os

# Function to convert JSON back to text
def json_to_text(input_file, output_dir=None):
    # Extract filename without extension and directory
    file_dir, file_name = os.path.split(input_file)
    name_without_ext = os.path.splitext(file_name)[0]

    # Determine output file location
    if output_dir:
        output_file = os.path.join(output_dir, name_without_ext + '.txt')
    else:
        output_file = os.path.join(file_dir, name_without_ext + '.txt')

    with open(input_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    with open(output_file, 'w', encoding='utf-8') as file:
        for key in sorted(json_data, key=int):
            file.write(json_data[key] + '\n')

# Check if input file and optionally output directory are provided as command-line arguments
if len(sys.argv) == 2:
    input_filename = sys.argv[1]
    json_to_text(input_filename)
elif len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_directory = sys.argv[2]
    json_to_text(input_filename, output_directory)
else:
    print("Usage: python json_to_text.py input.json [output_directory]")
