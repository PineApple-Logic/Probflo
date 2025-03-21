import ast
import pandas as pd
import math
from collections import defaultdict
import numpy as np

def interpolate_state(natural_flow, data):
    keys = sorted(data.keys())
    if natural_flow in data:
        return [natural_flow, 1.0, data[natural_flow]]  # Exact match with probability 1.0

    lower = max([k for k in keys if k <= natural_flow], default=keys[0])
    upper = min([k for k in keys if k >= natural_flow], default=keys[-1])

    if lower == upper:
        return [lower, 1.0, data[lower]]

    # Linear interpolation
    weight_upper = (natural_flow - lower) / (upper - lower)
    weight_lower = 1 - weight_upper

    return [lower, weight_lower, data[lower]], [upper, weight_upper, data[upper]]

def AVERAGE(array: list):
    return sum(array) / len(array)

def MAX(array: list):
    if not isinstance(array, (list, np.ndarray)) or len(array) == 0:
        return None
    return max(array)

def sum_duplicate_probabilities(values, probabilities):
    combined = defaultdict(float)
    for value, prob in zip(values, probabilities):
        combined[value] += prob

    sorted_keys = sorted(combined.keys())
    total_prob = sum(combined.values())

    # Normalize probabilities
    for key in sorted_keys:
        combined[key] /= total_prob  # Normalize to sum close to 1

    return list(combined.keys()), list(combined.values())

def process_and_adjust_probabilities(data, all_keys):
    adjusted_data = []

    for item in data:
        # Extract the probabilities
        values = item.strip("{}").split(", ")
        entries = [value.split(" ") for value in values]
        probabilities = [float(entry[1]) for entry in entries]
        numeric_values = [float(entry[0]) for entry in entries]

        # Check for missing keys and add them with a preset value
        missing_keys = [key for key in all_keys if key not in numeric_values]
        for missing_key in missing_keys:
            entries.append([str(missing_key), "0.001"])
            probabilities.append(0.001)
            numeric_values.append(missing_key)

        # Sort the entries based on numeric values
        sorted_indices = sorted(range(len(numeric_values)), key=lambda k: numeric_values[k])
        sorted_entries = [entries[i] for i in sorted_indices]
        sorted_probabilities = [probabilities[i] for i in sorted_indices]

        # Calculate the total and adjust if necessary
        total = sum(sorted_probabilities)
        if total != 1.0:
            smallest_index = sorted_probabilities.index(max(sorted_probabilities))
            adjustment = 1.0 - total
            sorted_probabilities[smallest_index] += adjustment

        # Reassemble the adjusted data
        adjusted_item = "{" + ", ".join([f"{sorted_entries[i][0]} {sorted_probabilities[i]:.3f}" for i in range(len(sorted_entries))]) + "}"
        adjusted_data.append(adjusted_item)

    return adjusted_data

def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        all_values = df.iloc[:, 1:].values.flatten()

        max_num = MAX(all_values)
        z = math.log(max_num) / math.log(25)

        percentiles = df.iloc[:, 1:].quantile([0.1, 0.2, 0.5, 0.8, 0.99]).mean(axis=1).tolist()

        DISCHARGE_LF = [AVERAGE(df.iloc[-i, 1:].values) for i in [3, 6, 8, 10, 12]]
        DISCHARGE_HF = [AVERAGE(df.iloc[i, 1:].values) for i in [-1, -3, -6, -8, -10]]
        DISCHARGE_FD = [MAX(df.iloc[i, 1:].values) for i in range(1, 6)]

        data = {
            0.0: 'A', 0.9: 'B', 1.8: 'C', 2.7: 'D', 3.6: '1', 4.6: '2',
            11.1: '3', 20.9: '4', 34.2: '5', 51.0: '6', 71.5: '7', 95.8: '8',
            124.0: '9', 156.3: '10', 192.6: '11', 233.1: '12', 277.9: '13',
            327.0: '14', 380.4: '15', 438.2: '16', 500.6: '17', 567.5: '18',
            638.9: '19', 715.0: '20', 795.8: '21', 881.3: '22', 971.6: '23',
            1066.7: '24', 1166.6: '25'
        }

        discharge_values = {}
        default_probabilities = [0.05, 0.2, 0.5, 0.2, 0.05]

        for key, values in {"YR": percentiles, "LF": DISCHARGE_LF, "HF": DISCHARGE_HF, "FD": DISCHARGE_FD}.items():
            interpolated_states = []
            probabilities = []

            for val, prob in zip(values, default_probabilities):
                interpolated = interpolate_state(val, data)
                for state in interpolated:
                    interpolated_states.append(state[0])
                    probabilities.append(state[1] * prob)

            unique_values, summed_probabilities = sum_duplicate_probabilities(interpolated_states, probabilities)

            # Create discharge values strings
            discharge_values[key] = "{" + ", ".join(
                [f"{val} {prob:.3f}" for val, prob in zip(unique_values, summed_probabilities)]) + "}"

        # Ensure the probabilities are adjusted and sum to 1 before returning
        all_keys = sorted(data.keys())
        final_data = process_and_adjust_probabilities(list(discharge_values.values()), all_keys)
        return final_data

    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

if __name__ == "__main__":
    import pathlib
    import os

    current_dir = pathlib.Path(__file__).resolve().parent
    excel_file_path = os.path.join(current_dir, 'test.xlsx')
    results = read_excel_file(excel_file_path)
    print(results)