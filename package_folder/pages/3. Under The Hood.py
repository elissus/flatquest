import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV
data_path = "../notebooks/berlin_cleaned.csv"
df = pd.read_csv(data_path)

# Streamlit page configuration
st.set_page_config(
    page_title = '3. Under The Hood',
    layout = 'wide'
)

st.title("Under The Hood")

st.markdown('''**The data:**''')
st.markdown('''- Kaggle dataset: 270k rental properties in Germany''')
st.markdown('''- 50 features (describe a few examples), including their addresses''')
st.markdown('''- We did some preprocessing, like dropping empty columns, etc.''')
st.markdown('''- After the cleaning we had a dataset of 8.000 properties in Berlin''')

# Create columns for the interactive widgets
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Add a slider for number of rooms
    max_rent = st.sidebar.slider(
        label = 'Max Total Rent (€)',
        min_value = int(df['totalRent'].min()),
        max_value = int(df['totalRent'].max()),
        value = int(df['totalRent'].max())
    )

with col2:
    # Add a slider for number of rooms
    rooms = st.sidebar.slider(
        label = 'Number of rooms',
        min_value = int(df['noRooms'].min()),
        max_value = int(df['noRooms'].max()),
        value = int(df['noRooms'].median())
    )

with col3:
    # Add a dropdown for selecting balcony
    newlyConst = st.sidebar.selectbox(
        label = 'newlyConst',
        options=df['newlyConst'].dropna().unique(),
        index=0
    )

# Filter data based on selection
filtered_df = df[(df['noRooms'] == rooms) & (df['newlyConst'] == newlyConst) & (df['totalRent'] <= max_rent)]

# Create a scatter plot
fig_scatter = px.scatter(
    filtered_df,
    x='livingSpace',
    y='totalRent',
    color='typeOfFlat',
    size='noRooms',
    title="Scatterplot of Living Space vs. Total Rent",
    labels={'livingSpace': 'Living Space (m²)', 'totalRent': 'Total Rent (€)'},
    hover_data=['fullAddress']
)

# Show the plot
st.plotly_chart(fig_scatter, use_container_width=True)

# Additional information
st.write(
    """
    Use the sliders to select the number of rooms and the maximum total rent,
    and the dropdown to choose the building's contruction status. The scatter plot will update based on the selections.
    """
)

st.markdown('''**Introducing geo features**''')
st.markdown('''- Geocoded all addresses into latitude & longitude''')
st.markdown('''- Create a function that calls the OpenStreetMap Overpass API:
    for a given coordinate, retrieve information on all locations within a given
    radius of each property. Locations can be parks, gyms, public transit
    stations, cafes, restaurants, etc.''')
st.markdown('''- We included the information on nearby places as extra features
    in our dataset Rental price prediction model''')
st.markdown('''- For each property, we estimated whether the rental price asked
    is “Above average”, “Average”, or “Below Average”. This estimation is based
    on a logistic regression model that uses the following features to predict:''')
