import overpy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut
import pandas as pd
import argparse
import math
#from google.cloud import bigquery

# function to geocode an address into latitude and longitude
def geocode_address(address: str, timeout: int = 10):
    '''Receives an address with street name, number, zip code, city and country
    and returns latitude and longitude'''
    geolocator = Nominatim(user_agent="measurements", timeout=timeout)
    try:
        location = geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            print(f"Geocoding failed for address: {address}")
            return None, None
    except GeocoderTimedOut:
        print(f"Geocoding timed out for address: {address}")
        return None, None


# function to calculate the distance in meters between two coordinates
def calculate_distance(coord1, coord2):
    '''Receives two coordinates and returns the distance between them in meters'''
    return geodesic(coord1, coord2).kilometers


def encode_density(place_type, count_of_places):
    density_ranges = {
        'restaurant': {'H': 15, 'M': 10, 'L': 5},
        'bar': {'H': 10, 'M': 5, 'L': 0},
        'gym': {'H': 5, 'M': 2, 'L': 0},
        'park': {'H': 25, 'M': 20, 'L': 10},
        'cafe': {'H': 15, 'M': 10, 'L': 5},
        'hospital': {'H': 2, 'M': 1, 'L': 0},
        'school': {'H': 2, 'M': 1, 'L': 0},
        'transit': {'H': 2, 'M': 1, 'L': 0}
    }

    ranges = density_ranges.get(place_type.lower())
    if not ranges:
        return 'N/A'

    if count_of_places > ranges['H']:
        return 'High'
    elif count_of_places > ranges['M']:
        return 'Medium'
    else:
        return 'Low'


# function to places of a given type within a radius of a given address
def find_nearby_places(address:str, place_type:str, radius:int=500, limit: int = 30):
    '''Function to find places of a specific type near a given address and radius in meters.
    Available place types are: "restaurant", "bar", "gym", "park", "cafe", "hospital", "school"'''
    latitude, longitude = geocode_address(address)
    origin = (latitude, longitude)

    # Initialize the Overpass API
    api = overpy.Overpass()

    # Define place type mapping to appropriate OSM tags
    place_type_mapping = {
        'restaurant': '[amenity=restaurant]',
        'bar': '[amenity=pub]',
        'gym': '[leisure=fitness_centre]',
        'park': '[leisure=park]',
        'cafe': '[amenity=cafe]',
        'hospital': '[amenity=hospital]',
        'school': '[amenity=school]',
        'transit': '[railway=station]'
    }

    # Get the appropriate OSM tag for the given place type
    osm_tag = place_type_mapping.get(place_type.lower())

    if not osm_tag:
        raise ValueError(f"Unsupported place type: {place_type}")

     # Formulate the Overpass API query
    query = f"""
    [out:json];
    (
        node{osm_tag}(around:{radius},{latitude},{longitude});
        way{osm_tag}(around:{radius},{latitude},{longitude});
        relation{osm_tag}(around:{radius},{latitude},{longitude});
    );
    out center {limit};
    """

    # Query the Overpass API
    result = api.query(query)

    # Store results in a list
    places = []

    for node in result.nodes:
        node_coords = (node.lat, node.lon)
        distance = calculate_distance(origin, node_coords)
        places.append({
            'name': node.tags.get('name', 'N/A'),
            'latitude': node.lat,
            'longitude': node.lon,
            'distance': distance
        })

    for way in result.ways:
        if way.center_lat is not None and way.center_lon is not None:
            way_coords = (way.center_lat, way.center_lon)
            distance = calculate_distance(origin, way_coords)
            places.append({
                'name': way.tags.get('name', 'N/A'),
                'latitude': way.center_lat,
                'longitude': way.center_lon,
                'distance': distance
            })

    for relation in result.relations:
        if relation.center_lat is not None and relation.center_lon is not None:
            relation_coords = (relation.center_lat, relation.center_lon)
            distance = calculate_distance(origin, relation_coords)
            places.append({
                'name': relation.tags.get('name', 'N/A'),
                'latitude': relation.center_lat,
                'longitude': relation.center_lon,
                'distance': distance
            })

    # Sort the list by distance
    places_sorted = sorted(places, key=lambda x: x['distance'])

    # Calculate the count of places and the average distance
    count_of_places = len(places_sorted)

    if count_of_places > 0:
        average_distance = sum([place['distance'] for place in places_sorted]) / count_of_places
    else:
        average_distance = 0

    # Calculate the area of the search circle in square meters
    area = math.pi * ((radius/1000)** 2)

    # Calculate the density score
    #if count_of_places > 0:
    #    #inverse_distance_sum = sum([1 / place['distance']/1000 for place in places_sorted if place['distance'] > 0])
    #    density = (count_of_places / area)
    #else:
    #    density = 0

    # encode density
    encoded_density = encode_density(place_type, count_of_places)

    print(places_sorted)
    print(f"Count of places: {count_of_places}")
    print(f"Area: {area}")
    print(f"Average distance: {average_distance:.2f} kilometers")
    #print(f"Density: {density} per square kilometer")
    print(f"Encoded density: {encoded_density}")

    return pd.DataFrame(places_sorted)#, density, average_distance

# Function to query a csv based Dataframe of the flats.
def find_best_matches(df, no_rooms, total_rent, living_space, balcony, top_n=10):
    # Calculate similarity score for each entry
    df['similarity_score'] = (abs(df['noRooms'] - no_rooms) +
                              abs(df['totalRent'] - total_rent) / total_rent +
                              abs(df['livingSpace'] - living_space) / living_space +
                              (df['balcony'] != balcony).astype(int))

    # Sort the DataFrame by similarity score
    sorted_df = df.sort_values('similarity_score')

    # Return the top N entries or as many as available
    best_matches = sorted_df.head(min(top_n, len(sorted_df)))

    # Drop the similarity score column for the final output
    return best_matches.drop(columns=['similarity_score'])

def main():
    parser = argparse.ArgumentParser(description="Find nearby places of a specific type.")
    parser.add_argument("address", type=str, help="The address to search near.")
    parser.add_argument("place_type", type=str, help="The type of place to search for (e.g., restaurant, gym, park).")
    parser.add_argument("--radius", type=int, default=500, help="The search radius in meters. Default is 500 meters.")

    args = parser.parse_args()

    try:
       find_nearby_places(args.address, args.place_type, args.radius)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
