import csv
import json
import os


def json_to_csv(json_file):
    no_extension = os.path.splitext(json_file)[0]
    csv_file = f'./assets/data/Dataframe/{no_extension}.csv'   # Specify your CSV output file here
    json_file = os.path.join('./conf', json_file)
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Prepare data for CSV
    headers = ['Node', 'Zero', 'Low', 'Med', 'High']
    rows = []

    for key, values in data.items():
        row = [key]  # Start with the main key (Node)
        for header in headers[1:]:
            row.append(values.get(header, ''))
        rows.append(row)

    # Write data to CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Write the header row
        writer.writerows(rows)    # Write the data rows
    os.remove(json_file)


if __name__ == "__main__":
    os.chdir('../../')  # Change directory to the correct location
    json = input('Json file name to convert:')
    json_to_csv(json)
