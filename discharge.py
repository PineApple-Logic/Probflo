import pandas as pd
import math
from icecream.icecream import ic as console_trace


def find_closest_state(natural_flow):
    data = {
        0.0: 'A',
        0.9: 'B',
        1.8: 'C',
        2.7: 'D',
        3.6: '1',
        4.6: '2',
        11.1: '3',
        20.9: '4',
        34.2: '5',
        51.0: '6',
        71.5: '7',
        95.8: '8',
        124.0: '9',
        156.3: '10',
        192.6: '11',
        233.1: '12',
        277.9: '13',
        327.0: '14',
        380.4: '15',
        438.2: '16',
        500.6: '17',
        567.5: '18',
        638.9: '19',
        715.0: '20',
        795.8: '21',
        881.3: '22',
        971.6: '23',
        1066.7: '24',
        1166.6: '25',
    }

    # Find the closest natural flow value
    closest_flow = min(data.keys(), key=lambda x: abs(x - natural_flow))
    
    # Retrieve the corresponding state
    closest_state = data[closest_flow]

    return [closest_flow,2, closest_state]

def AVERAGE(array:list):
    return sum(array) / len(array)


def MAX(array: list):
    if not array:return None 
    max_value = array[0]
    for element in array:
        if element > max_value:
            max_value = element
    return max_value



def read_excel_file(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Display the entire DataFrame
        # print("Contents of the Excel file:")
        # print(df)

        # Get all values (excluding the first column) as a flattened array
        all_values = df.iloc[:, 1:].values.flatten()

        # Calculate percentiles
        

        max_num =  MAX(list(all_values))
        
        z = math.log(max_num)/math.log(25)
        
        i = 14 # i is the row number
        formula = math.pow(i-3,z)
        print("=================> ",formula)
        # print("========================\n\n",z)


        percentiles = pd.Series(all_values).quantile([0.1, 0.2, 0.5, 0.8, 0.99]) # FOR DISCHARGE_YR
        

        DISCHARGE_YR_1 = pd.Series(all_values).quantile(0.1)
        DISCHARGE_YR_2 = pd.Series(all_values).quantile(0.2)
        DISCHARGE_YR_3 = pd.Series(all_values).quantile(0.5)
        DISCHARGE_YR_4 = pd.Series(all_values).quantile(0.8)
        DISCHARGE_YR_5 = pd.Series(all_values).quantile(0.99)
        console_trace(DISCHARGE_YR_1)

        DISCHARGE_LF_1 = AVERAGE(all_values[-3:]) 
        print(DISCHARGE_YR_1)
        DISCHARGE_LF_2 = AVERAGE([df['Jul'].iloc[-3],df['Aug'].iloc[-3],df['Sep'].iloc[-3]])
        DISCHARGE_LF_3 = AVERAGE([df['Jul'].iloc[-6],df['Aug'].iloc[-6],df['Sep'].iloc[-6]])
        DISCHARGE_LF_4 = AVERAGE([df['Jul'].iloc[-8],df['Aug'].iloc[-8],df['Sep'].iloc[-8]])
        DISCHARGE_LF_5 = AVERAGE([df['Jul'].iloc[-10],df['Aug'].iloc[-10],df['Sep'].iloc[-10]])
        

        DISCHARGE_HF_1 = AVERAGE([df['Jan'].iloc[-1],df['Feb'].iloc[-1],df['Mar'].iloc[-1]]) 
        DISCHARGE_HF_2 = AVERAGE([df['Jan'].iloc[-3],df['Feb'].iloc[-3],df['Mar'].iloc[-3]])
        DISCHARGE_HF_3 = AVERAGE([df['Jan'].iloc[-6],df['Feb'].iloc[-6],df['Mar'].iloc[-6]])
        DISCHARGE_HF_4 = AVERAGE([df['Jan'].iloc[-8],df['Feb'].iloc[-8],df['Mar'].iloc[-8]])
        DISCHARGE_HF_5 = AVERAGE([df['Jan'].iloc[-10],df['Feb'].iloc[-10],df['Mar'].iloc[-10]])
        
        DISCHARGE_FD_1 = MAX([df['Jan'].iloc[5],df['Feb'].iloc[5],df['Mar'].iloc[5]])
        DISCHARGE_FD_2 = MAX([df['Jan'].iloc[4],df['Feb'].iloc[4],df['Mar'].iloc[4]])
        DISCHARGE_FD_3 = MAX([df['Jan'].iloc[3],df['Feb'].iloc[3],df['Mar'].iloc[3]])
        DISCHARGE_FD_4 = MAX([df['Jan'].iloc[2],df['Feb'].iloc[2],df['Mar'].iloc[2]])
        DISCHARGE_FD_5 = MAX([df['Jan'].iloc[1],df['Feb'].iloc[1],df['Mar'].iloc[1]])
        # console_trace(DISCHARGE_FD_1,DISCHARGE_FD_2,DISCHARGE_FD_3,DISCHARGE_FD_4,DISCHARGE_FD_5) 

        # DISCHARGE_YR_CALC = f"{DISCHARGE_YR_1} {find_closest_state(DISCHARGE_YR_1)[0]} {DISCHARGE_YR_2} {find_closest_state(DISCHARGE_YR_2)[0]} {DISCHARGE_YR_3} {find_closest_state(DISCHARGE_YR_3)[0]} {DISCHARGE_YR_4} {find_closest_state(DISCHARGE_YR_4)[0]} {DISCHARGE_YR_5} {find_closest_state(DISCHARGE_YR_5)[0]}"  
        # DISCHARGE_LF_CALC = f"{DISCHARGE_LF_1} {find_closest_state(DISCHARGE_LF_1)[0]} {DISCHARGE_LF_2} {find_closest_state(DISCHARGE_YR_2)[0]} {DISCHARGE_YR_3} {find_closest_state(DISCHARGE_YR_3)[0]} {DISCHARGE_YR_4} {find_closest_state(DISCHARGE_YR_4)[0]} {DISCHARGE_YR_5} {find_closest_state(DISCHARGE_YR_5)[0]}"  
        # DISCHARGE_HF_CALC = f"{DISCHARGE_LF_1} {find_closest_state(DISCHARGE_LF_1)[0]} {DISCHARGE_YR_2} {find_closest_state(DISCHARGE_YR_2)[0]} {DISCHARGE_YR_3} {find_closest_state(DISCHARGE_YR_3)[0]} {DISCHARGE_YR_4} {find_closest_state(DISCHARGE_YR_4)[0]} {DISCHARGE_YR_5} {find_closest_state(DISCHARGE_YR_5)[0]}"  
        # DISCHARGE_FD_CALC = f"{DISCHARGE_LF_1} {find_closest_state(DISCHARGE_LF_1)[0]} {DISCHARGE_YR_2} {find_closest_state(DISCHARGE_YR_2)[0]} {DISCHARGE_YR_3} {find_closest_state(DISCHARGE_YR_3)[0]} {DISCHARGE_YR_4} {find_closest_state(DISCHARGE_YR_4)[0]} {DISCHARGE_YR_5} {find_closest_state(DISCHARGE_YR_5)[0]}"  
        
        fcs = find_closest_state
        DY1,DY2,DY3,DY4,DY5 =  fcs(DISCHARGE_YR_1)[0],fcs(DISCHARGE_YR_2)[0],fcs(DISCHARGE_YR_3)[0],fcs(DISCHARGE_YR_4)[0],fcs(DISCHARGE_YR_5)[0]
        FD1,FD2,FD3,FD4,FD5 =  fcs(DISCHARGE_FD_1)[0],fcs(DISCHARGE_FD_2)[0],fcs(DISCHARGE_FD_3)[0],fcs(DISCHARGE_FD_4)[0],fcs(DISCHARGE_FD_5)[0]
        LD1,LD2,LD3,LD4,LD5 =  fcs(DISCHARGE_LF_1)[0],fcs(DISCHARGE_LF_2)[0],fcs(DISCHARGE_LF_3)[0],fcs(DISCHARGE_LF_4)[0],fcs(DISCHARGE_LF_5)[0]
        HF1,HF2,HF3,HF4,HF5 =  fcs(DISCHARGE_HF_1)[0],fcs(DISCHARGE_HF_2)[0],fcs(DISCHARGE_HF_3)[0],fcs(DISCHARGE_HF_4)[0],fcs(DISCHARGE_HF_5)[0]
        
        discharge_values = {
            "YR" :f'{DY1} 0.05, {DY2} 0.2, {DY3} 0.5, {DY4} 0.2, {DY5} 0.05',
            "LF" :f'{LD1} 0.05, {LD2} 0.2, {LD3} 0.5, {LD4} 0.2, {LD5} 0.05',
            "HF" :f'{HF1} 0.05, {HF2} 0.2, {HF3} 0.5, {HF4} 0.2, {HF5} 0.05',
            "FD" :f'{FD1} 0.05, {FD2} 0.2, {FD3} 0.5, {FD4} 0.2, {FD5} 0.05',
        }
        for discharge in discharge_values:
            discharge_values[discharge] = "{"+discharge_values[discharge]+"}"
        console_trace(discharge_values)
       
       
        # DISCHARGE_YR_CALC = f"{DISCHARGE_LF_1} {find_closest_state(DISCHARGE_LF_1)[0]} {DISCHARGE_YR_2} {find_closest_state(DISCHARGE_YR_2)[0]} {DISCHARGE_YR_3} {find_closest_state(DISCHARGE_YR_3)[0]} {DISCHARGE_YR_4} {find_closest_state(DISCHARGE_YR_4)[0]} {DISCHARGE_YR_5} {find_closest_state(DISCHARGE_YR_5)[0]}"  
        

        d = discharge_values
        return d["YR"]+"++"+d["LF"]+"++"+d["HF"]+"++"+d["FD"]

    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    import pathlib
    import os
    current_dir = pathlib.Path(__file__).resolve().parent
    # Replace 'testfile.xlsx' with the actual path to your Excel file
    excel_file_path =  os.path.join(current_dir,'testfile.xlsx')    
    # Call the function to read the Excel file
    data_frame = read_excel_file(excel_file_path)
        
    # You can now use 'data_frame' to perform further operations with the data
