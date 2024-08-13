import pandas as pd
import geo
import argparse
import time
import os



def load_apartment_data(file_path: str):
    """Loads the apartment dataset from a CSV file."""
    return pd.read_csv(file_path)#, nrows=5)

# Example function to process a single category for all apartments
def process_category_for_apartments(df, category, radius=500, limit=30, delay=3.6):
    """Processes a single category for all apartments in the DataFrame."""
    df[f'{category}_places'] = None
    df[f'{category}_density'] = None

    for i, row in df.iterrows():
        address = row['fullAddress']  # assuming the column name for the address is 'address'
        places_df = geo.find_nearby_places(address, category, radius, limit)

        # Create a list of dictionaries for nearby places
        nearby_places = places_df.to_dict(orient='records')

        # Calculate density encoding
        density = geo.encode_density(category, len(nearby_places))

        # Store results in the DataFrame
        df.at[i, f'{category}_places'] = nearby_places
        df.at[i, f'{category}_density'] = density

        # Print the counter to track progress
        print(f"Processed {i + 1} out of {len(df)} apartments.")

        # Pause to avoid exceeding API rate limit
        time.sleep(delay)

    return df

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Process nearby places for apartments.")
    #parser.add_argument('--file_path', type=str, required=True, help="Path to the apartment data CSV file.")
    parser.add_argument('--category', type=str, required=True, help="Place category to search for (e.g., restaurant, gym).")
    parser.add_argument('--radius', type=int, default=500, help="Search radius in meters (default: 500).")
    #parser.add_argument('--output_file', type=str, default="output.csv", help="Path to save the output CSV (default: output.csv).")

    args = parser.parse_args()
    file_path = "berlin_cleaned.csv"

    # Load the first 20 apartments
    apartment_df = load_apartment_data(file_path)

    # Process the specified category
    updated_df = process_category_for_apartments(apartment_df, args.category, args.radius)

    # Generate the output file path dynamically, saving it in the ../notebooks/geo_features/ directory
    output_dir = os.path.join(os.path.dirname(__file__), "..", "notebooks", "geo_features")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"berlin_{args.category}.csv")

    # Save the updated DataFrame to a CSV file
    updated_df.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()
