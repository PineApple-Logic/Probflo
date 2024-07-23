import pandas as pd
import os


def create_excel(excel_file_path):
    # List of nodes
    nodes = [
        "LIV_VEG_PRED", "DOM_WAT_GRO", "FLO_ATT_UPS", "WAT_DIS_HUM", "WAT_DIS_PRED",
        "SEASON_BASE", "SEASON_FRESH", "NO_BARRIERS", "AQ_ALIENS_PRED", "AQ_ALIENS_COMP",
        "LANDUSE_SSUP", "VEG_ECO_ACOMP", "REC_SPIR_WILD", "TOURISM_ACC", "RES_RES_CFLO",
        "TOURISM_POT", "REC_SPIR_POT", "INV_ECO_POT", "VEG_ECO_POT", "FISH_ECO_POT",
        "RES_RES_POT", "WAT_DIS_DPOT", "WAT_DIS_CPOT", "RIV_ASS_POT", "FLO_ATT_POT",
        "DOM_WAT_DEM", "LIV_VEG_POT", "SUB_VEG_POT", "SUB_FISH_POT", "WQ_ECOSYSTEM",
        "WQ_LIVESTOCK", "WQ_PEOPLE", "WQ_TREATMENT", "DISCHARGE_YR", "DISCHARGE_LF",
        "DISCHARGE_HF", "DISCHARGE_FD"
    ]

    # Check for file existence and create a unique file name if needed
    base_path, ext = os.path.splitext(excel_file_path)
    counter = 1
    new_excel_file_path = excel_file_path
    while os.path.exists(new_excel_file_path):
        new_excel_file_path = f"{base_path}({counter}){ext}"
        counter += 1

    # Create a DataFrame with a single row
    df = pd.DataFrame([nodes])

    df.to_excel(new_excel_file_path, index=False, header=False)

    return new_excel_file_path


def add_string_below_node(excel_file_path, node_name, string_to_add):
    # Load the existing Excel file
    df = pd.read_excel(excel_file_path, header=None)

    # Check if the node_name is in the DataFrame
    if node_name in df.iloc[0].values:
        # Find the index of the node_name
        node_index = df.iloc[0].tolist().index(node_name)

        # Ensure the DataFrame has space for the new row
        if len(df) < 2:
            df.loc[1] = [None] * len(df.columns)

        # Add the string_to_add in the second row under the specified node
        df.iloc[1, node_index] = string_to_add

        # Save the updated DataFrame to the same Excel file
        df.to_excel(excel_file_path, index=False, header=False)
        print(f'String "{string_to_add}" added below "{node_name}" in the Excel file.')
    else:
        print(f'Node "{node_name}" not found in the Excel file.')


if __name__ == '__main__':
    os.chdir('../../')
    # Example usage

    # create excel
    new_path = create_excel('./Downloads/test.xlsx')

    # edit excel
    add_string_below_node(new_path, 'DOM_WAT_GRO', 'Hello')
    add_string_below_node(new_path, 'FLO_ATT_UPS', 'Hello')
