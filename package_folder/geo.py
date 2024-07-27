import overpy
from geopy.geocoders import Photon
from geopy.distance import geodesic
import pandas as pd
import argparse


# function to geocode an address into latitude and longitude
def geocode_address(address:str):
    '''Receives an address with street name, number, zip code, city and country
    and returns latitude and longitude'''
    geolocator = Photon(user_agent="measurements")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude


# function to calculate the distance in meters between two coordinates
def calculate_distance(coord1, coord2):
    '''Receives two coordinates and returns the distance between them in meters'''
    return geodesic(coord1, coord2).meters


# function to places of a given type within a radius of a given address
def find_nearby_places(address:str, place_type:str, radius:int=500):
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
        'school': '[amenity=school]'
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
    out center;
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
    print(places_sorted)

    return places_sorted #pd.DataFrame(places_sorted)

def main():
    parser = argparse.ArgumentParser(description="Find nearby places of a specific type.")
    parser.add_argument("address", type=str, help="The address to search near.")
    parser.add_argument("place_type", type=str, help="The type of place to search for (e.g., restaurant, gym, park).")
    parser.add_argument("--radius", type=int, default=500, help="The search radius in meters. Default is 500 meters.")

    args = parser.parse_args()

    try:
        nearby_places = find_nearby_places(args.address, args.place_type, args.radius)
        for place in nearby_places:
            print(f"Place: {place['name']}, Lat: {place['latitude']}, Lon: {place['longitude']}, Distance: {place['distance']:.6f} degrees")
            print("Tags:")
            for key, value in place['tags'].items():
                print(f"  {key}: {value}")
            print()
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
