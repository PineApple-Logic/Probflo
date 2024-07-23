from streamlit_option_menu import option_menu
from assets.Pages.Graphs import Graphs
from assets.Pages.Generate import Generate
import streamlit as st


# Tab menu
st.set_page_config(
    page_title="Probflo Risk Assessment",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="auto",
)

select = option_menu(
    menu_title='Probflo Risk Assessment',
    options=["Graphs", "Generate"],
    icons=["graph-up", "globe-europe-africa"],
    default_index=0,
    orientation="horizontal",
)

if select == "Graphs":
    Graphs()
elif select == "Generate":
    Generate()
else:
    Graphs()
