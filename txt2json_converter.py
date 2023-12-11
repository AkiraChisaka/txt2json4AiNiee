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

# Convert text file to JSON
def convert_to_json(input_file, output_file):
    global counter
    counter = 1  # Reset counter for each file conversion

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    json_dict = {}
    for line in lines:
        if line.strip():
            line_to_json(line, json_dict)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_dict, file, ensure_ascii=False, indent=4)

# Convert JSON back to text
def json_to_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    with open(output_file, 'w', encoding='utf-8') as file:
        for key in sorted(json_data, key=int):
            file.write(json_data[key] + '\n')

# Main function to decide the conversion type
def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <1 for converting to JSON / 2 for text> <input file> [output directory]")
        return

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_directory = sys.argv[3] if len(sys.argv) > 3 else None

    file_dir, file_name = os.path.split(input_file)
    name_without_ext = os.path.splitext(file_name)[0]

    if output_directory:
        output_file = os.path.join(output_directory, name_without_ext)
    else:
        output_file = os.path.join(file_dir, name_without_ext)

    if mode == '1':
        output_file += '.json'
        convert_to_json(input_file, output_file)
    elif mode == '2':
        output_file += '.txt'
        json_to_text(input_file, output_file)
    else:
        print("Invalid mode. Use 1 for converting to JSON and 2 for converting to text.")

if __name__ == "__main__":
    main()
