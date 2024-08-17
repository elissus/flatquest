import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import geo
import query
import data_extraction as dax

# Initialize session state
if 'map' not in st.session_state:
    st.session_state['map'] = None
if 'first_query' not in st.session_state:
    st.session_state['first_query'] = None
if 'results' not in st.session_state:
    st.session_state['results'] = None
if 'addresses' not in st.session_state:
    st.session_state['addresses'] = None

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the header image
relative_path = os.path.join("frontend_data", "flatquest_header.jpg")

# Construct the absolute path
image_path = os.path.join(current_dir, relative_path)

# Display the header image
st.image(image_path, use_column_width=True)

# Title and description
st.title("Find an apartment")


# Defining empty variables to prevent Streamlit from printing Error Messages for not existing variables
results = []
result = {}
addresses = []
requested_categories = {}
selected_result = []

# Define unique categories
categories = [
    'restaurant',
    'bar',
    'gym',
    'park',
    'cafe',
    'hospital',
    'school',
    'transit'
]

# Allow the user to select categories of interest using checkboxes in rows
selected_categories = []
category_density = {}

  # Define colors for each category
category_colors = {
        'restaurant': 'purple',
        'bar': 'blue',
        'gym': 'orange',
        'park': 'green',
        'cafe': 'brown',
        'hospital': 'red',
        'school': 'yellow',
        'transit': 'grey'
    }

total_rent = st.text_input("Enter desired total rent in €", key="total rent")

living_space = st.text_input("Enter desired living space in m²", key="living space")

no_rooms = st.text_input("Enter desired number of rooms", key="no rooms")

balcony = st.radio("Do you want a balcony?", ('yes', 'no'), index=1)

# Data conversion and validation
try:
    total_rent = float(total_rent) if total_rent else None
except ValueError:
    st.error("Please enter a valid number for total rent.")

try:
    living_space = float(living_space) if living_space else None
except ValueError:
    st.error("Please enter a valid number for living space.")

try:
    no_rooms = float(no_rooms) if no_rooms else None
except ValueError:
    st.error("Please enter a valid integer for number of rooms.")

balcony = True if balcony == 'yes' else False



st.write("Please select your places of interest")

# Track the number of selected checkboxes
selected_count = 0

# Slider options
options = ["Low", "Medium", "High"]

for i in range(0, len(categories), 3):
    cols = st.columns(3)
    for j, category in enumerate(categories[i:i + 3]):
        with cols[j]:
            if selected_count < 3:
                selected = st.checkbox(category, key=f"checkbox_{category}", value=False)
                if selected:
                    selected_categories.append(category)
                    selected_count += 1
                    density = st.select_slider("Select desired number:", options=options, key=f"slider_{category}")
                    category_density[category] = density
            else:
                st.checkbox(category, value=False, key=f"checkbox_{category}", disabled=True)

# API Request

#df = pd.read_csv("berlin_cleaned.csv")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "berlin_merged.csv"))

#df = query.query_bq()

# Define the button to trigger the process
if st.button('Submit'):
    # Call dax.find_best_matches_2 to get the DataFrame of apartments
    apartment_df = dax.find_best_matches_2(df, no_rooms, total_rent, living_space, balcony, selected_categories, category_density, top_n=10)

    # Store the addresses for later use
    st.session_state['addresses'] = apartment_df['fullAddress'].tolist()

    # Initialize an empty list to store all results
    all_poi_results = []

    # Iterate over each row in the DataFrame
    #for i in range(len(apartment_df)):
        # Get the row-specific data transformed by dax.transform_data
    row_data = dax.transform_row(apartment_df)

        # Flatten the row data and append it to the all_poi_results list
    for key, value in row_data.items():
        all_poi_results.append(value)

    st.session_state['results'] = all_poi_results

    # Create a dictionary to hold the final results for map plotting
    final_results = {}

    # Iterate over the apartment addresses and corresponding POI results
    for i in range(len(st.session_state['addresses'])):
        address = st.session_state['addresses'][i]
        address_results = []

        # Extract the results for the current apartment
        poi_data = st.session_state['results'][i]

        # Iterate over the categories (restaurant, gym, transit)
        for category, pois in poi_data.items():
            for poi_list in pois:
                for poi in poi_list:
                    # Create a POI dictionary with necessary details
                    poi_info = {
                        'name': poi['name'],
                        'latitude': poi['latitude'],
                        'longitude': poi['longitude'],
                        'category': category
                    }
                    address_results.append(poi_info)

        # Store the results for the current apartment
        final_results[f'Apartment {i+1}'] = address_results[:20]  # Limit to 20 POIs per apartment

    # Create a folium map centered at a default location (Berlin)
    mymap = folium.Map(location=[52.5200, 13.4050], zoom_start=12)

    # Add apartment addresses to the map
    for i, address in enumerate(st.session_state['addresses']):
        try:
            address_coords = geo.geocode_address(address)  # Assuming this function returns latitude and longitude
            if address_coords is None:
                st.warning(f"Skipping address {address} - could not geocode")
                continue  # Skip this address if geocoding fails

            # Add a marker for the apartment address
            folium.Marker(
                location=address_coords,
                popup=f"Address: {address}",
                icon=folium.Icon(color='blue')
            ).add_to(mymap)

        except Exception as e:
            st.error(f"An error occurred while geocoding the address {address}: {e}")
            continue  # Skip this address if an error occurs

    for key, pois in final_results.items():
        for poi in pois:
            category = poi['category']
            color = category_colors.get(category, 'black')  # Default to black if category color is not defined
            folium.CircleMarker(
                location=[poi['latitude'], poi['longitude']],
                radius=5,  # Smaller radius
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f"{poi['name']} ({poi['category']})"
            ).add_to(mymap)

    # Store the map in session state
    st.session_state['map'] = mymap

# Display the map if it exists in session state
if 'map' in st.session_state and st.session_state['map'] is not None:
    st_folium(st.session_state['map'], width='100%', height=700)


# Footer
st.markdown("---")
st.markdown("Developed by FlatQuest Team | Powered by [Streamlit](https://streamlit.io) and [Folium](https://python-visualization.github.io/folium/).")
