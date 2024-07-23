import ast
import pandas as pd
import math
from collections import defaultdict


def find_closest_state(natural_flow):
    data = {
        0.0: 'A', 0.9: 'B', 1.8: 'C', 2.7: 'D', 3.6: '1', 4.6: '2',
        11.1: '3', 20.9: '4', 34.2: '5', 51.0: '6', 71.5: '7', 95.8: '8',
        124.0: '9', 156.3: '10', 192.6: '11', 233.1: '12', 277.9: '13',
        327.0: '14', 380.4: '15', 438.2: '16', 500.6: '17', 567.5: '18',
        638.9: '19', 715.0: '20', 795.8: '21', 881.3: '22', 971.6: '23',
        1066.7: '24', 1166.6: '25',
    }

    # Find the closest natural flow value
    closest_flow = min(data.keys(), key=lambda x: abs(x - natural_flow))

    # Retrieve the corresponding state
    closest_state = data[closest_flow]

    return [closest_flow, 2, closest_state]


def AVERAGE(array: list):
    return sum(array) / len(array)


def MAX(array: list):
    if not array:
        return None
    max_value = array[0]
    for element in array:
        if element > max_value:
            max_value = element
    return max_value


def sum_duplicate_probabilities(values, probabilities):
    combined = defaultdict(float)
    for value, prob in zip(values, probabilities):
        combined[value] += prob
    return list(combined.keys()), list(combined.values())


def read_excel_file(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Get all values (excluding the first column) as a flattened array
        all_values = df.iloc[:, 1:].values.flatten()

        # Calculate percentiles
        max_num = MAX(list(all_values))
        z = math.log(max_num) / math.log(25)

        i = 14  # i is the row number
        formula = math.pow(i - 3, z)
        print("=================> ", formula)

        percentiles = pd.Series(all_values).quantile([0.1, 0.2, 0.5, 0.8, 0.99])  # FOR DISCHARGE_YR

        DISCHARGE_YR = [pd.Series(all_values).quantile(p) for p in [0.1, 0.2, 0.5, 0.8, 0.99]]
        DISCHARGE_LF = [
            AVERAGE(all_values[-3:]),
            AVERAGE([df['Jul'].iloc[-3], df['Aug'].iloc[-3], df['Sep'].iloc[-3]]),
            AVERAGE([df['Jul'].iloc[-6], df['Aug'].iloc[-6], df['Sep'].iloc[-6]]),
            AVERAGE([df['Jul'].iloc[-8], df['Aug'].iloc[-8], df['Sep'].iloc[-8]]),
            AVERAGE([df['Jul'].iloc[-10], df['Aug'].iloc[-10], df['Sep'].iloc[-10]])
        ]
        DISCHARGE_HF = [
            AVERAGE([df['Jan'].iloc[-1], df['Feb'].iloc[-1], df['Mar'].iloc[-1]]),
            AVERAGE([df['Jan'].iloc[-3], df['Feb'].iloc[-3], df['Mar'].iloc[-3]]),
            AVERAGE([df['Jan'].iloc[-6], df['Feb'].iloc[-6], df['Mar'].iloc[-6]]),
            AVERAGE([df['Jan'].iloc[-8], df['Feb'].iloc[-8], df['Mar'].iloc[-8]]),
            AVERAGE([df['Jan'].iloc[-10], df['Feb'].iloc[-10], df['Mar'].iloc[-10]])
        ]
        DISCHARGE_FD = [
            MAX([df['Jan'].iloc[5], df['Feb'].iloc[5], df['Mar'].iloc[5]]),
            MAX([df['Jan'].iloc[4], df['Feb'].iloc[4], df['Mar'].iloc[4]]),
            MAX([df['Jan'].iloc[3], df['Feb'].iloc[3], df['Mar'].iloc[3]]),
            MAX([df['Jan'].iloc[2], df['Feb'].iloc[2], df['Mar'].iloc[2]]),
            MAX([df['Jan'].iloc[1], df['Feb'].iloc[1], df['Mar'].iloc[1]])
        ]

        discharge_values = {
            "YR": [find_closest_state(val)[0] for val in DISCHARGE_YR],
            "LF": [find_closest_state(val)[0] for val in DISCHARGE_LF],
            "HF": [find_closest_state(val)[0] for val in DISCHARGE_HF],
            "FD": [find_closest_state(val)[0] for val in DISCHARGE_FD]
        }

        default_probabilities = [0.05, 0.2, 0.5, 0.2, 0.05]
        discharge_strings = {}
        for key, values in discharge_values.items():
            unique_values, summed_probabilities = sum_duplicate_probabilities(values, default_probabilities)
            discharge_strings[key] = "{" + ", ".join([f"{val} {prob}" for val, prob in zip(unique_values, summed_probabilities)]) + "}"
        print(discharge_strings)

        # Convert to list
        string = ', '.join(discharge_strings.values())
        cleaned_string = string.strip('{}')
        parts = cleaned_string.split('}, {')
        formatted_list = [f"{{{part}}}" for part in parts]
        result = [f'{item}' for item in formatted_list]
        return result

    except Exception as e:
        print(f"Error reading Excel file: {e}")


if __name__ == "__main__":
    import pathlib
    import os

    current_dir = pathlib.Path(__file__).resolve().parent
    # Replace 'testfile.xlsx' with the actual path to your Excel file
    excel_file_path = os.path.join(current_dir, 'test.xlsx')
    # Call the function to read the Excel file
    results = read_excel_file(excel_file_path)
    # You can now use 'data_frame' to perform further operations with the data
    print(results)
