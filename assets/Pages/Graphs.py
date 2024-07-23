import streamlit as st
import os
from assets.Scripts.Graphs_page_scripts import save_uploaded_file, process_data, load_graph


def Graphs():
    """
    Creates visuals for page and executes scripts as needed
    """

    st.selectbox('Select a Netica module', ['Balule'])

    # File upload widget, restricted to Excel files, disallow multiple file uploads
    uploaded_file = st.file_uploader("Upload Excel case file", type=["xlsx", "xls"], accept_multiple_files=False)

    if uploaded_file is not None:
        # Save Data
        save_uploaded_file(uploaded_file)

        # Process data
        try:
            no_extension = process_data(uploaded_file)
        except Exception as e:
            st.error(f'Failed to process data: {e}')
            os.remove(f'./Uploads/{uploaded_file.name}')
            return

        # Load Graph
        load_graph(no_extension)
