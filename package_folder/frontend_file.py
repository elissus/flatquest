
import streamlit as st
import pandas as pd
from decimal import Decimal
import folium
from streamlit_folium import st_folium
import requests
import os
from st_aggrid import AgGrid, GridOptionsBuilder
import geo


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the header image
relative_path = os.path.join("frontend_data", "flatquest_header.jpg")

# Construct the absolute path
image_path = os.path.join(current_dir, relative_path)


# Display the header image
st.image(image_path, use_column_width=True)

# Title and description
st.title("Find an appartment")

# Sample data - replace with your database query or CSV file
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
          "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]

# Convert list to DataFrame
cities_df = pd.DataFrame(cities, columns=["City"])

#Defining empty variables to prevent Streamlit from printing Error Messages for not existing variables
results = []
result = {}
addresses =[]
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

balcony = st.radio(f"Do you want a balcony?", ('yes', 'no'), index=1)

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

# Display the inputs and their types
#st.write(f"Total Rent: {total_rent} (type: {type(total_rent)})")
#st.write(f"Living Space: {living_space} (type: {type(living_space)})")
#st.write(f"Number of Rooms: {no_rooms} (type: {type(no_rooms)})")
#st.write(f"Balcony: {balcony} (type: {type(balcony)})")

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
        'transit']

# Allow the user to select categories of interest using checkboxes in rows
selected_categories = []
category_density = {}


st.write("Please select your places of interest")

# Track the number of selected checkboxes
selected_count = 0

#Slider options
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
                    #density = st.radio(f"Density for {category}", ('high', 'medium', 'low'), index=1)
                    # Create a slider with custom options
                    density = st.select_slider("Select desired number:", options=options, key=f"slider_{category}")
                    category_density[category] = density
            else:
                st.checkbox(category, value=False, key=f"checkbox_{category}", disabled=True)

#API Request

# Initialize a flag to control visibility of results and map
show_results = False

df = pd.read_csv("/home/hsinbyushin/code/elissus/flatquest/notebooks/berlin_cleaned.csv")

# Button to trigger the API call
if st.button('Submit'):
    first_query = geo.find_best_matches(df, no_rooms, total_rent, living_space, balcony, top_n=10)
    st.write(first_query)

    # Prepare the data for the API call
    requested_categories = {
        'selected_categories': selected_categories,
        'category_density': category_density
    }

    addresses = first_query['fullAddress'].tolist()

# Define categories and prepare results storage
results = []

# Iterate over each address
for address in addresses:
    # List to hold results for different categories for the current address
    address_results = []

    # Iterate over each category
    for category in selected_categories:
        # Call the API and store the results for the current category
        category_results = geo.find_nearby_places(address, category)
        address_results.append(category_results)

    # Store the results for the current address
    results.append(address_results)

    show_results = True
    # Display the API response
    #if response.status_code == 200:
     #   st.success("API call successful!")
      #  st.json(response.json())
      #  show_results = True
    #else:
    #    st.error(f"API call failed with status code {response.status_code}")

# Flag to show results
show_results = True


# Only display results and map if show_results is True
if show_results:
    # Example list of dictionaries for different results
    # Initialisiere ein leeres Dictionary, um die Ergebnisse zu speichern
    final_results = {}

   # Iteriere über die Adressen
    for i in range(len(addresses)):
        address_results = []  # Liste zur Speicherung der Ergebnisse für die aktuelle Adresse
        for j in range(len(selected_categories)):  # Iteriere über die Kategorien
            if len(results[i]) > j:  # Überprüfe, ob die Ergebnisse für die Kategorie existieren
                if 'name' in results[i][j]:  # Überprüfe, ob der Schlüssel 'name' existiert
                    for k in range(len(results[i][j]['name'])):  # Iteriere über die Points of Interest
                        poi = {
                            'name': results[i][j]['name'][k],
                            'latitude': results[i][j]['latitude'][k],
                            'longitude': results[i][j]['longitude'][k],
                            'category': selected_categories[j]
                        }
                        address_results.append(poi)
        # Füge die Ergebnisse für die aktuelle Adresse zum finalen Ergebnis hinzu
        final_results[f'Appartment {i+1}'] = address_results

# Convert each list of dictionaries to a DataFrame
dataframes = {key: pd.DataFrame(value) for key, value in final_results.items()}

# Convert Decimal columns to float, if they exist
for df in dataframes.values():
    if not df.empty and 'latitude' in df.columns and 'longitude' in df.columns:
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)

# Allow the user to select a result
selected_result = st.selectbox('Select a result:', list(dataframes.keys()))

if selected_result:
    selected_df = dataframes[selected_result]
    st.dataframe(selected_df)


# Create a folium map centered around the selected points of interest
if not selected_df.empty:
    map_center = [selected_df['latitude'].mean(), selected_df['longitude'].mean()]
    mymap = folium.Map(location=map_center, zoom_start=14)

# Define colors for each category
category_colors = {
    'gym': 'red',
    'restaurant': 'purple',
    'school': 'blue',
    'bar': 'yellow',
    'park': 'green',
    'cafe': 'brown',
    'hospital': 'white',
    'transit': 'grey'
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
