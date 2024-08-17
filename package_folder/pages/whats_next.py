import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

city_image = os.path.join(current_dir, "..", "frontend_data", "city.webp")
platform_image = os.path.join(current_dir, "..", "frontend_data", "platform.webp")
global_image = os.path.join(current_dir, "..", "frontend_data", "global.jpeg")
pig_image = os.path.join(current_dir, "..", "frontend_data", "pig.jpg")

# Streamlit page configuration
st.set_page_config(
    page_title = 'Under The Hood',
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



st.markdown('<p class="big-font">The FlatQuest Vision</p>', unsafe_allow_html=True)
st.write("")

col1, spacer, col2 = st.columns([1, 0.2, 1])

with col1:
    st.markdown("### Making FlatQuest more Powerful")
    st.image(city_image)
    #st.write("Popular neighborhoods are in high demand, leading to limited availability and inflated prices, forcing many to settle for less desirable options.")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("### Expand its reach")
    st.image(global_image)

with col2:
    st.markdown("### Turn it into a vertically integrated rental property platform")
    st.image(platform_image)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("### Monetization Strategies")
    st.image(pig_image)
