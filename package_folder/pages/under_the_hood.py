import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data from CSV
#data_path = "../notebooks/berlin_cleaned.csv"
df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "berlin_cleaned.csv"))
drop_columns = ['Unnamed: 0', 'telekomUploadSpeed', 'scoutId']
df_hm = df.drop(columns=drop_columns)

current_dir = os.path.dirname(os.path.abspath(__file__))

kaggle_image = os.path.join(current_dir, "..", "frontend_data", "kaggle.png")
pie_image = os.path.join(current_dir, "..", "frontend_data", "pie.png")
osm_image = os.path.join(current_dir, "..", "frontend_data", "osm.png")
latitude_image = os.path.join(current_dir, "..", "frontend_data", "latitude.jpg")
geocoding_image = os.path.join(current_dir, "..", "frontend_data", "geocoding.png")
forest_image = os.path.join(current_dir, "..", "frontend_data", "forest.png")
heatmap_image = os.path.join(current_dir, "..", "frontend_data", "heatmap.png")


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

st.markdown(
    """
    <style>
    .header-text {
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title
st.markdown('<p class="big-font">The Rental Properties dataset</p>', unsafe_allow_html=True)
st.write("")


# Creating two columns
col1, spacer, col2 = st.columns([1, 0.2, 1])

with col1:
    st.image(kaggle_image)

with col2:
    data_text = "We used a Kaggle dataset with 270k rental properties scraped from Immoscout24, the biggest real estate platform in Germany. The data is property of Immoscout24 and is for research purposes only."
    st.write("")
    st.markdown(f'<p class="header-text">{data_text}</p>', unsafe_allow_html=True)

st.write("")
#col3, spacer, col4 = st.columns([1, 0.2, 1])

#with col3:
st.image(pie_image, caption="For the purpose of our project, we limited to Berlin data. From 270k we are left with 9k properties")
st.write("")
st.write("")
st.write("")

fig_scatter = px.scatter(
    df,
    x='livingSpace',
    y='totalRent',
    size='noRooms',
    range_x= [10, 300],
    range_y= [1, 5000],
    title="Scatterplot of Living Space vs. Total Rent",
    labels={'livingSpace': 'Living Space (m²)', 'totalRent': 'Total Rent (€)'},
    size_max=50
)

# Update the font size for the entire chart and the title
fig_scatter.update_layout(
    height=800,
    font=dict(
        family="Courier New, monospace",  # Font family
        size=50,  # Adjust this value for the overall font size
        color="RebeccaPurple"  # Font color
    ),
    title=dict(
        font=dict(
            size=30  # Adjust this value for the title font size
        )
    )
)

# Show the plot in Streamlit
st.plotly_chart(fig_scatter, use_container_width=True)


st.markdown('<p class="big-font">The Rental Price prediction model</p>', unsafe_allow_html=True)

# Create a heatmap



col3, spacer2, col4 = st.columns([1, 0.2, 1])



with col3:
    st.write("")
    st.write("")
    st.write("")
    st.markdown(f"""
    <p class="header-text">
        1. Identify key features<br>
        2. Remove outliers<br>
        3. Scale numerical features<br>
        4. Select best model
    </p>
    """, unsafe_allow_html=True)

with col4:
    st.image(forest_image)


st.image(heatmap_image)
st.write("")
st.write("")

st.markdown('<p class="big-font">Enriching with Geospatial features</p>', unsafe_allow_html=True)
st.write("")
geo_text = f"""
    Our main advantage vs. the popular rental platforms: we allow users to include neighborhood parameters into their seach query.
    This way, users find the apartment that fits their needs close to places that are important to their lifestyle.

"""
st.markdown(f'<p class="header-text">{geo_text}</p>', unsafe_allow_html=True)
st.write("")
st.write("")
st.image(geocoding_image)
