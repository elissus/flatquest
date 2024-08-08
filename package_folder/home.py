import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import geo

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

# Sample data - replace with your database query or CSV file
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
          "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]

# Convert list to DataFrame
cities_df = pd.DataFrame(cities, columns=["City"])

# Defining empty variables to prevent Streamlit from printing Error Messages for not existing variables
results = []
result = {}
addresses = []
requested_categories = {}
selected_result = []

# Create an input field with autocomplete
def city_autocomplete():
    input_city = st.text_input("Enter city name", key="city_input")
    if input_city:
        # Filter cities based on input
        filtered_cities = cities_df[cities_df['City'].str.contains(input_city, case=False, na=False)]

        if not filtered_cities.empty:
            selected_city = st.radio(
                "Suggestions",
                filtered_cities['City'].tolist(),
                key="suggestions_radio"
            )
            return selected_city

    return input_city

selected_city = city_autocomplete()

if selected_city:
    st.write(f"You selected: {selected_city}")

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

if selected_city:
    st.write(f"You selected: {selected_city}")

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

st.write("Please select your places of interest")

# Track the number of selected checkboxes
selected_count = 0

# Slider options
options = ["Some", "Average", "Many"]

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

df = pd.read_csv("../notebooks/berlin_cleaned.csv")

# Button to trigger the API call
if st.button('Submit'):
    st.session_state['first_query'] = geo.find_best_matches(df, no_rooms, total_rent, living_space, balcony, top_n=10)
    #st.write(st.session_state['first_query'])

    # Prepare the data for the API call
    requested_categories = {
        'selected_categories': selected_categories,
        'category_density': category_density
    }

    st.session_state['addresses'] = st.session_state['first_query']['fullAddress'].tolist()

    results = []

    # Iterate over each address
    for address in st.session_state['addresses']:
        # List to hold results for different categories for the current address
        address_results = []

        # Iterate over each category
        for category in selected_categories:
            # Call the API and store the results for the current category
            category_results = geo.find_nearby_places(address, category)
            address_results.append(category_results)

        # Store the results for the current address
        results.append(address_results)

    st.session_state['results'] = results

    # Create the map only after the results are ready
    final_results = {}

    # Iterate over the addresses
    for i in range(len(st.session_state['addresses'])):
        address_results = []  # List to store results for the current address
        for j in range(len(selected_categories)):  # Iterate over the categories
            if len(st.session_state['results'][i]) > j:  # Check if results for the category exist
                if 'name' in st.session_state['results'][i][j]:  # Check if the 'name' key exists
                    for k in range(len(st.session_state['results'][i][j]['name'])):  # Iterate over the points of interest
                        poi = {
                            'name': st.session_state['results'][i][j]['name'][k],
                            'latitude': st.session_state['results'][i][j]['latitude'][k],
                            'longitude': st.session_state['results'][i][j]['longitude'][k],
                            'category': selected_categories[j]
                        }
                        address_results.append(poi)
        final_results[f'Apartment {i+1}'] = address_results[:5]  # Limit to 5 points of interest

    # Create a folium map
    mymap = folium.Map(location=[52.5200, 13.4050], zoom_start=12)  # Centered at Berlin for example

    # Add addresses and points of interest to the map
    for address in st.session_state['addresses']:
        address_coords = geo.geocode_address(address)  # Assuming this function returns the latitude and longitude
        folium.Marker(
            location=address_coords,
            popup=f"Address: {address}",
            icon=folium.Icon(color='blue')
        ).add_to(mymap)

    # Add points of interest to the map
    for key, pois in final_results.items():
        for poi in pois:
            folium.CircleMarker(
                location=[poi['latitude'], poi['longitude']],
                radius=5,  # Smaller radius
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.7,
                popup=f"{poi['name']} ({poi['category']})"
            ).add_to(mymap)

    # Store the map in session state
    st.session_state['map'] = mymap

# Display the map if it exists in session state
if st.session_state['map'] is not None:
    st_folium(st.session_state['map'], width=700, height=500)

# Footer
st.markdown("---")
st.markdown("Developed by [Your Name](https://yourwebsite.com) | Powered by [Streamlit](https://streamlit.io) and [Folium](https://python-visualization.github.io/folium/).")
