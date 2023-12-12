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

# Combines 2 JSON files together
def combine_json_files(json_file1, json_file2, output_file):
    with open(json_file1, 'r', encoding='utf-8') as file:
        json_data1 = json.load(file)

    with open(json_file2, 'r', encoding='utf-8') as file:
        json_data2 = json.load(file)

    combined_json = {}
    max_len = max(len(json_data1), len(json_data2))

    for i in range(1, max_len + 1):
        key = str(i)
        if key in json_data1 and json_data1[key].strip():  # If key exists and is not empty in json_data1
            combined_json[key] = json_data1[key]
        elif key in json_data2:  # If key exists in json_data2 (regardless of whether it's empty)
            combined_json[key] = json_data2[key]

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(combined_json, file, ensure_ascii=False, indent=4)

# Main function to decide the conversion type
def main():
    if len(sys.argv) < 3:
        print_general_usage()
        return

    mode = sys.argv[1]

    if mode == '1' or mode == '2':
        if len(sys.argv) < 3:
            print("Usage: python script.py " + mode + " <input file> [output directory]")
            return
        input_file = sys.argv[2]
        output_directory = sys.argv[3] if len(sys.argv) > 3 else None
        extension = '.json' if mode == '1' else '.txt'
        output_file = get_output_file(input_file, output_directory, extension, append_char='c')
        convert_to_json(input_file, output_file) if mode == '1' else json_to_text(input_file, output_file)

    elif mode == '3':
        if len(sys.argv) < 4:
            print("Usage: python script.py 3 <json_file1> <json_file2> [output file]")
            return
        json_file1 = sys.argv[2]
        json_file2 = sys.argv[3]
        output_file = sys.argv[4] if len(sys.argv) > 4 else get_output_file(json_file1, None, '.json', append_char='m')
        combine_json_files(json_file1, json_file2, output_file)

    else:
        print_general_usage()

# Stuff for the main function
def get_output_file(input_file, output_directory, extension, append_char=''):
    file_dir, file_name = os.path.split(input_file)
    name_without_ext = os.path.splitext(file_name)[0] + append_char
    if output_directory:
        return os.path.join(output_directory, name_without_ext + extension)
    else:
        return os.path.join(file_dir, name_without_ext + extension)

# Stuff for error
def print_general_usage():
    print("Usage: python script.py <mode> <required arguments based on mode>")
    print("Modes:")
    print("1 - Convert to JSON: python script.py 1 <input file> [output directory]")
    print("2 - Convert to Text: python script.py 2 <input JSON file> [output directory]")
    print("3 - Combine JSON files: python script.py 3 <json_file1> <json_file2> [output file]")

if __name__ == "__main__":
    main()
