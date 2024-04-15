import pandas as pd
import math
import openpyxl
from icecream.icecream import ic as console
import ast
MAXIMA = 100

import re

def replace_values_with_hashtag(node_value):
    # Define a regular expression pattern to match digits or digits with decimal point followed by a space
    pattern = r'(\d+(\.\d+)?)\s'
    # Define a function to replace matched groups with '#pn' followed by the matched groups and a space
    def replace(match):
        return f'#{match.group(1)} '
    # Use the sub() function from re module to replace matched patterns
    return re.sub(pattern, replace, node_value)





def find_differences(array1, array2):
    set1 = set(array1)
    set2 = set(array2)
    only_in_array1 = set1 - set2
    only_in_array2 = set2 - set1
    return list(only_in_array1), list(only_in_array2)
class ExcelProcessor:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.data_frame = self.read_excel_file()

    def read_excel_file(self):
        df = pd.read_excel(self.excel_file_path)
        return df

    def remove_empty_columns(self):
        self.data_frame = self.data_frame.dropna(axis=1, how='all')

    def remove_rows_with_all_nan(self):
        self.data_frame = self.data_frame.dropna(axis=0, how='all')

    def get_values_array(self):
        columns_array = self.data_frame.columns.tolist()
        values_array = self.data_frame.values.flatten()

        values_array = [value for value in values_array if pd.notna(value)]
        values_array = list(map(lambda val: val.replace("}", "").replace("{", "").split(","), values_array))

        return columns_array, values_array

    def process_values_array(self, columns_array, values_array):
        mappings = {}
        mappings["IDnum"] = [str(i) for i in range(MAXIMA)]
           
        for key, val in enumerate(values_array):
            mappings[columns_array[key]] = []

            for i in range(len(val)):
                distribution = val[i].strip().rstrip().split()
                state_name = distribution[0]
                distribution_val = math.ceil(float(distribution[1]) * MAXIMA)

                for _ in range(distribution_val):
                    mappings[columns_array[key]].append(state_name)
        # console(mappings)
        return mappings

    def create_excel_with_columns(self, data, excel_filename='output.xlsx'):
        df = pd.DataFrame(data)
        df.to_excel(excel_filename, index=False)
        print(f"Excel file '{excel_filename}' created successfully.")

    def write_to_text_file(self, excel_filename, output_file_path="output.cas"):
        workbook = openpyxl.load_workbook(excel_filename)
        sheet = workbook.active

        with open(output_file_path, "w") as output_file:
            for row in sheet.iter_rows():
                row_data = [str(cell.value) for cell in row]
                output_line = '\t'.join(row_data) + '\n'
                output_file.write(output_line)


# Example usage:
def process_excel_file(input_excel, output_excel='example.xlsx', output_text='output.cas'):
    excel_processor = ExcelProcessor(input_excel)
    # console(excel_processor.data_frame)
    excel_processor.remove_empty_columns()
    excel_processor.remove_rows_with_all_nan()

    columns_array, values_array = excel_processor.get_values_array()
    mappings = excel_processor.process_values_array(columns_array, values_array)
    excel_processor.create_excel_with_columns(mappings, excel_filename=output_excel)
    excel_processor.write_to_text_file(excel_filename=output_excel, output_file_path=output_text)
    df = pd.read_excel(input_excel)
    # console(output_excel)
    columns_dict = {}
    for column in df.columns:
        columns_dict[column] = df[column].tolist()
    for node in columns_dict:
        columns_dict[node] = str(columns_dict[node][0]).split(",")
        columns_dict[node] = list(map(lambda state: state.strip().rstrip(),columns_dict[node]))
        columns_dict[node] = ",".join(columns_dict[node])[1:-1]
        

        # columns_dict[node] = columns_dict[node].split(",")
        # for i in range(len(columns_dict[node])):
            # columns_dict[node][i] = columns_dict[node][i].split(":")
            # columns_dict[node][i][0] = f"\"{columns_dict[node][i][0]}\""
        #     columns_dict[node][i] = ":".join(columns_dict[node][i])
        # columns_dict[node] = ",".join(columns_dict[node])   
        # columns_dict[node] = eval("{"+columns_dict[node]+"}")
    # console(columns_dict)

    key_to_remove = 'Unnamed: 31'
    if key_to_remove in columns_dict:
        value = columns_dict.pop(key_to_remove)
    else:
        print(f"Key '{key_to_remove}' doesn't exist in the dictionary, doing nothing.")
    
    with open("output.cas", "w") as f: 
        nodenames = columns_dict.keys()
        
        for key,val in columns_dict.items():
            if columns_dict[key][0].isdigit():
               tmp = columns_dict[key] 
               columns_dict[key] = "{"+tmp+"}"
            else: 
                columns_dict[key] = "{" + val + "}"
            
            columns_dict[key] = columns_dict[key].replace(',', ', ')
               
               
        values = columns_dict.values()

        f.write("\t".join(nodenames)+"\n"+"\t".join(values)) 
    return "output.cas"
# Example usage of the function:
 