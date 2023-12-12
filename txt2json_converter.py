import json
import sys
import os

# Convert text file to JSON
def convert_to_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    json_dict = {}
    current_entry = ""
    new_paragraph = False

    for line in lines:
        if line.strip():  # If line contains text
            if new_paragraph:
                # Remove only the last newline character
                if current_entry.endswith('\n'):
                    current_entry = current_entry[:-1]
                json_dict[str(len(json_dict) + 1)] = current_entry
                current_entry = line
                new_paragraph = False
            else:
                current_entry += line
        else:  # Line is empty (i.e., contains only a newline)
            if current_entry.strip():  # Check if there's text before this empty line
                new_paragraph = True
            current_entry += line  # Add the newline to the current entry

    if current_entry.strip():  # Add any remaining text to the json_dict
        # Remove only the last newline character
        if current_entry.endswith('\n'):
            current_entry = current_entry[:-1]
        json_dict[str(len(json_dict) + 1)] = current_entry

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_dict, file, ensure_ascii=False, indent=4)

# Convert JSON back to text
def json_to_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    with open(output_file, 'w', encoding='utf-8') as file:
        last_key = str(len(json_data))  # Get the last key to avoid extra newlines at the end
        for key in sorted(json_data, key=int):
            file.write(json_data[key])
            if key != last_key:  # Avoid adding an extra newline at the end of the file
                file.write('\n')  # Add a newline to separate entries

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
