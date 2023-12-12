# Text-to-JSON Converter

## Description
This Python script is designed to convert text files into JSON format, specifically tailored for preserving the original formatting of novels, including line breaks and special characters. It also includes functionality to convert JSON back into text and to combine two JSON files, prioritizing content from one file and filling in gaps with content from the second file.

## Installation
No installation is required. The script runs in any Python environment. Ensure you have Python installed on your system. You can download Python from [here](https://www.python.org/downloads/).

## Usage
The script can be run from the command line with the following commands:

### Convert Text to JSON
```
python script.py 1 <input file> [output directory]
```
This will convert the input text file into a JSON file, preserving formatting like line breaks. The 'c' character is appended to the output file name.

### Convert JSON to Text
```
python script.py 2 <input JSON file> [output directory]
```
This will convert the input JSON file back into a text file, maintaining the original formatting.

### Combine JSON Files
```
python script.py 3 <json_file1> <json_file2> [output file]
```
This combines two JSON files. It takes the content from the first file and fills in gaps using the second file. If the output file name is not specified, the 'm' character is appended to the first file's name for the output file.
