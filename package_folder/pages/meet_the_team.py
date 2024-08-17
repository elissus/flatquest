import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

team = os.path.join(current_dir, "..", "frontend_data", "team.png")

# Streamlit page configuration
st.set_page_config(
    page_title = 'Meet the Team',
    layout = 'wide'
)

st.markdown("""
    <style>
    /* Change the font size for all text */
    body, div, p {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .big-font {
        font-size:50px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown('<p class="big-font">Meet the Team</p>', unsafe_allow_html=True)
st.write("")

st.image(team)
