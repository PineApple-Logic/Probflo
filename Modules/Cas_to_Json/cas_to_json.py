import json
import os
import pandas as pd


def is_text_file(filepath):
    """Check if a file is a text file by reading a small chunk and trying to decode it."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            file.read(512)  # Read the first 512 bytes
        return True
    except (UnicodeDecodeError, IOError):
        return False


def parse_text_file(input_file, encoding='utf-8'):
    try:
        with open(input_file, 'r', encoding=encoding) as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        # Retry with a different encoding if utf-8 fails
        with open(input_file, 'r', encoding='latin-1') as file:
            lines = file.readlines()

    if len(lines) < 2:
        return None  # Not enough data to process

    header = lines[0].strip().split('\t')
    data = lines[1].strip().split('\t')

    result = {}
    for key, value in zip(header, data):
        value = value.strip('{}').split(', ')
        sub_dict = {}
        for item in value:
            if ' ' in item:
                k, v = item.split(' ', 1)
                try:
                    sub_dict[k] = float(v)
                except ValueError:
                    continue  # Skip items that can't be converted to float
        result[key] = sub_dict

    return result


def parse_excel_file(input_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # The first row is considered as header and the second row as the data
    header = df.columns.tolist()
    data = df.iloc[0].tolist()

    result = {}
    for key, value in zip(header, data):
        value = value.strip('{}').split(', ')
        sub_dict = {}
        for item in value:
            if ' ' in item:
                k, v = item.split(' ', 1)
                try:
                    sub_dict[k] = float(v)
                except ValueError:
                    continue  # Skip items that can't be converted to float
        result[key] = sub_dict

    return result


def write_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


# List all files in the 'Uploads' directory
input_files = os.listdir('../../Uploads/')

# Process each file in the 'Uploads' directory
for file in input_files:
    input_path = os.path.join('../../Uploads', file)
    if file.endswith('.xlsx'):
        data = parse_excel_file(input_path)
    elif is_text_file(input_path):
        data = parse_text_file(input_path)
    else:
        print(f"Skipping non-text or non-Excel file: {file}")
        continue

    if data:
        output_file = f'{file.rsplit(".", 1)[0]}.json'
        write_to_json(data, f'../../conf/{output_file}')
    else:
        print(f"Skipping file with insufficient data: {file}")

print("Conversion completed.")
