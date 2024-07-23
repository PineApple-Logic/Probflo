import streamlit as st
import os
from assets.Scripts.cas_to_json import main as cas_to_json
from assets.Scripts.json_to_csv import json_to_csv
from Modules.Netica_Modules.run import main as netica
import plotly.graph_objects as go
import pandas as pd

# Define the uploads directory
UPLOADS_DIR = os.path.abspath('./Uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Define the output directory
OUTPUT_DIR = os.path.abspath('./conf')
os.makedirs(OUTPUT_DIR, exist_ok=True)


# SCRIPTS
def save_uploaded_file(upload):
    if hasattr(upload, 'name'):
        file_path = os.path.join(UPLOADS_DIR, upload.name)
    else:
        st.error("Uploaded file does not have a name attribute.")
        return
    try:
        with open(file_path, "wb") as f:
            f.write(upload.getbuffer())
        st.success(f"File {upload.name} saved successfully!")
    except Exception as e:
        st.error(f"An error occurred while saving the file '{upload.name}': {e}")


def process_data(upload):
    st.info('Processing data, Please wait.')
    cas_to_json(upload.name)
    no_extension = os.path.splitext(upload.name)[0]
    netica(f'./conf/{no_extension}.json', f'./conf/end_{no_extension}.json')
    json_to_csv(f'end_{no_extension}.json')
    return no_extension


def load_graph(no_extension):
    wide_df = pd.read_csv(f'./assets/data/Dataframe/end_{no_extension}.csv')
    colors = {
        'Zero': 'white',
        'Low': 'white',
        'Med': 'orange',
        'High': 'red'
    }
    # Create the figure
    fig = go.Figure()

    # Add bars for each category, stacking them
    for category in ['High', 'Med', 'Low', 'Zero']:
        fig.add_trace(go.Bar(
            x=wide_df['Node'],
            y=wide_df[category],
            name=category,
            marker_color=colors[category]
        ))
    # Update the layout to set the title and stack the bars
    fig.update_layout(
        barmode='stack',
        title='Risk assessment',
        yaxis=dict(
            categoryorder='array',
            categoryarray=['High', 'Med', 'Low', 'Zero']
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    os.remove(f'./assets/data/Dataframe/end_{no_extension}.csv')
