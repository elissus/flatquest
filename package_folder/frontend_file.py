
import streamlit as st
import pandas as pd
from decimal import Decimal
import folium
from streamlit_folium import st_folium
import requests

# Title and description
st.title("📍 Location Display on Map")

# Define unique categories
categories = [
        'restaurant',
        'bar',
        'gym',
        'park',
        'cafe',
        'hospital',
        'school',
        'transit']

# Allow the user to select categories of interest using checkboxes in rows
selected_categories = []
category_density = {}

st.write("### Select Categories and Density")

st.write("Please select three categories of places of interest and choose a level of density for the search")

# Track the number of selected checkboxes
selected_count = 0

for i in range(0, len(categories), 3):
    cols = st.columns(3)
    for j, category in enumerate(categories[i:i + 3]):
        with cols[j]:
            if selected_count < 3:
                selected = st.checkbox(category, value=False)
                if selected:
                    selected_categories.append(category)
                    selected_count += 1
                    density = st.radio(f"Density for {category}", ('high', 'medium', 'low'), index=1)
                    category_density[category] = density
            else:
                st.checkbox(category, value=False, disabled=True)


#API Request

# Initialize a flag to control visibility of results and map
show_results = False


# Button to trigger the API call
if st.button('Submit'):
    # Prepare the data for the API call
    payload = {
        'selected_categories': selected_categories,
        'category_density': category_density
    }

    # Make the API call (replace 'http://example.com/api' with your actual API endpoint)
    response = requests.post('http://example.com/api', json=payload)

    # Display the API response
    if response.status_code == 200:
        st.success("API call successful!")
        st.json(response.json())
        show_results = True
    else:
        st.error(f"API call failed with status code {response.status_code}")

# Only display results and map if show_results is True
if show_results:
    # Example list of dictionaries for different results
    results = {
        'Result 1': [
            {'name': 'Bodystreet', 'latitude': Decimal('52.5079287'), 'longitude': Decimal('13.3917379'), 'address': 'Street 1, City', 'category': 'gym'},
            {'name': 'McFit', 'latitude': Decimal('52.5106479'), 'longitude': Decimal('13.3974279'), 'address': 'Street 2, City', 'category': 'gym'},
            {'name': 'Holmes Place', 'latitude': Decimal('52.5123998'), 'longitude': Decimal('13.3908216'), 'address': 'Street 3, City', 'category': 'gym'},
        ],
        'Result 2': [
            {'name': 'Restaurant A', 'latitude': Decimal('52.5099287'), 'longitude': Decimal('13.3957379'), 'address': 'Street 4, City', 'category': 'restaurant'},
            {'name': 'School B', 'latitude': Decimal('52.5086479'), 'longitude': Decimal('13.3934279'), 'address': 'Street 5, City', 'category': 'school'}
        ],
        # Add more results as needed...
    }

    # Convert each list of dictionaries to a DataFrame
    dataframes = {key: pd.DataFrame(value) for key, value in results.items()}

    # Convert Decimal columns to float
    for df in dataframes.values():
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)

    # Allow the user to select a result
    selected_result = st.selectbox('Select a result:', list(dataframes.keys()))

    # Get the selected DataFrame
    selected_df = dataframes[selected_result]

    # Display the selected DataFrame
    st.dataframe(selected_df)

    # Create a folium map centered around the selected points of interest
    if not selected_df.empty:
        map_center = [selected_df['latitude'].mean(), selected_df['longitude'].mean()]
        mymap = folium.Map(location=map_center, zoom_start=14)

        # Define colors for each category
        category_colors = {
            'gym': 'red',
            'restaurant': 'green',
            'school': 'blue'
        }

        # Add points of interest to the map
        for index, row in selected_df.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,  # Smaller radius
                color=category_colors.get(row['category'], 'black'),
                fill=True,
                fill_color=category_colors.get(row['category'], 'black'),
                fill_opacity=0.7,
                popup=f"{row['name']} ({row['category']})"
            ).add_to(mymap)

        # Display the map in Streamlit
        st_folium(mymap, width=700, height=500)

    # Fußzeile
    st.markdown("---")
    st.markdown("Developed by [Your Name](https://yourwebsite.com) | Powered by [Streamlit](https://streamlit.io) and [Folium](https://python-visualization.github.io/folium/).")
