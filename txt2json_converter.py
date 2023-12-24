import json
import sys
import os

# Convert text file to JSON
def convert_to_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    json_dict = {}
    current_entry = ""
    line_count = 0

    for line in lines:
        line_count += 1
        current_entry += line

        if not line.strip() or (line_count == len(lines)) or (line_count < len(lines) and lines[line_count].strip()):
            # Remove only one newline character from the end if present
            if current_entry.endswith('\n'):
                current_entry = current_entry[:-1]
            json_dict[str(len(json_dict) + 1)] = current_entry
            current_entry = ""  # Reset for the next entry

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

# Combines 2 JSON files and converts the result to text
def combine_and_convert_to_text(json_file1, json_file2, output_file_json, output_file_txt):
    combine_json_files(json_file1, json_file2, output_file_json)
    json_to_text(output_file_json, output_file_txt)

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
    print("4 - Combine JSON files and Convert to Text: python script.py 4 <json_file1> <json_file2> [output directory]")

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

    elif mode == '4':
        if len(sys.argv) < 4:
            print("Usage: python script.py 4 <json_file1> <json_file2> [output directory]")
            return
        json_file1 = sys.argv[2]
        json_file2 = sys.argv[3]
        output_directory = sys.argv[4] if len(sys.argv) > 4 else None
        output_file_json = get_output_file(json_file1, output_directory, '.json', append_char='m')
        output_file_txt = get_output_file(json_file1, output_directory, '.txt', append_char='mc')
        combine_and_convert_to_text(json_file1, json_file2, output_file_json, output_file_txt)

    else:
        print_general_usage()

if __name__ == "__main__":
    main()
