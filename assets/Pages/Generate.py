import os
import streamlit as st
from assets.data.nods_dictonary import data as nods
from assets.Scripts.table_to_discharge import read_excel_file as table_to_cas
from assets.Scripts.excel import create_excel, add_string_below_node
from assets.Scripts.Graphs_page_scripts import save_uploaded_file, process_data, load_graph

UPLOADS_DIR = os.path.abspath('./Uploads')
DOWNLOADS_DIR = os.path.abspath('./Downloads')
selected_values = {}

# Initialize session state variables
if 'output_file_path' not in st.session_state:
    st.session_state['output_file_path'] = None


def cleanup_files():
    # Cleanup function to remove the generated output file
    if 'output_file_path' in st.session_state:
        if st.session_state['output_file_path'] and os.path.exists(st.session_state['output_file_path']):
            os.remove(st.session_state['output_file_path'])
            st.session_state['output_file_path'] = None


def Generate():
    """
    Generate page visuals as well as executes scripts as needed
    """

    col1, col2, col3 = st.columns(3, vertical_alignment='top')
    with col1:
        st.markdown('### Node Name')
    with col2:
        st.markdown('### Questions')
    with col3:
        st.markdown('### Answer')

    st.markdown('---')
    # Body
    for key, value in nods.items():
        col1, col2, col3 = st.columns(3, vertical_alignment='center')
        with col1:
            st.success(f"{key}")
        with col2:
            st.info(f"{value['question']}")
        with col3:
            options = list(value['values'].keys())
            id = f"{key}"
            selected_values[id] = st.selectbox('', options, key=id)

    st.markdown('---')
    # Convert flow table to initial case file
    uploaded_file = st.file_uploader("Upload Excel Flow table", type=["xlsx", "xls"], accept_multiple_files=False)

    if uploaded_file is not None:
        # Save the uploaded file to UPLOADS_DIR
        upload_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
        save_uploaded_file(uploaded_file)
        data_from_table = table_to_cas(upload_path)

        # Create the output file in DOWNLOADS_DIR
        new_path = os.path.join(DOWNLOADS_DIR, 'output.xlsx')
        create_excel(new_path)

        try:
            add_string_below_node(new_path, 'DISCHARGE_YR', data_from_table[0])
            add_string_below_node(new_path, 'DISCHARGE_LF', data_from_table[1])
            add_string_below_node(new_path, 'DISCHARGE_HF', data_from_table[2])
            add_string_below_node(new_path, 'DISCHARGE_FD', data_from_table[3])
            os.remove(upload_path)  # Remove the uploaded file after processing

            # Update session state with the new output file path
            st.session_state['output_file_path'] = new_path

        except Exception as e:
            st.error('Incompatible data')
            os.remove(upload_path)  # Remove the uploaded file on error
            return

        st.markdown('---')

        # Complete case file generation
        if st.button('Generate case', use_container_width=True):
            for key, value in nods.items():
                string = nods[key]['values'][selected_values[key]]
                add_string_below_node(new_path, key, string)
            st.success('Case File Generated')

            st.markdown('---')

            with open(new_path, 'rb') as file:
                button = st.download_button(
                    'Download case file', file,
                    use_container_width=True,
                    file_name='case.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

            if button:
                os.remove(new_path)
                cleanup_files()  # Remove the generated case file after download

    # Clean up files on Streamlit rerun
    cleanup_files()
