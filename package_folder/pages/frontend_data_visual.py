import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV
data_path = "/Users/LinhVu/code/linhvu12/elissus/flatquest/notebooks/berlin_cleaned.csv"
df = pd.read_csv(data_path)

# Streamlit page configuration
st.set_page_config(
    page_title = 'Data Visualization',
    layout = 'wide'
)

# Page title
st.title('Data Visualization')

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
    color='balcony',
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

# Create a heatmap
st.subheader('Correlation Heatmap')
df_num = df.select_dtypes(include=['int64', 'float64'])
plt.figure(figsize=(10, 6))
sns.heatmap(df_num.corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap of numerial features')

# Show the heatmap
st.pyplot(plt)
