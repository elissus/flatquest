import json
import re
import pandas as pd



def find_best_matches_2(df, no_rooms, total_rent, living_space, balcony, selected_categories, category_density, top_n=10, density_penalty=1):
    # Calculate similarity score for each entry
    df['similarity_score'] = (abs(df['noRooms'] - no_rooms) +
                             abs(df['totalRent'] - total_rent) / total_rent +
                             abs(df['livingSpace'] - living_space) / living_space +
                              (df['balcony'] != balcony).astype(int))

    # Adjust similarity score based on category density preferences
    for cat, dens in zip(selected_categories, category_density):
        # Add penalty to similarity score if density doesn't match
        df['similarity_score'] += (df[cat + '_density'] != dens).astype(int) * density_penalty

    # Sort the DataFrame by similarity score
    sorted_df = df.sort_values('similarity_score')

    # Return the top N entries or as many as available
    best_matches = sorted_df.head(min(top_n, len(sorted_df)))

    # Drop the similarity score column for the final output
    return best_matches.drop(columns=['similarity_score'])



def transform_data(row):
    poi_categories = {
        'restaurant': row['restaurant_places'] if pd.notna(row['restaurant_places']) else [],
        'gym': row['gym_places'] if pd.notna(row['gym_places']) else [],
        'transit': row['transit_places'] if pd.notna(row['transit_places']) else [],
        'park': row['park_places'] if pd.notna(row['park_places']) else [],
        'bar': row['bar_places'] if pd.notna(row['bar_places']) else []
    }

    all_res = {}  # Dictionary to store results with category names as keys

    # Process each category
    for category_name, category_data in poi_categories.items():
        category_res = []  # To store results for the current category
        if category_data:  # Ensure category_data is not empty
            try:
                # Replace Decimal with float or string, and replace single quotes with double quotes
                clean_str = re.sub(r"Decimal\('([\d\.]+)'\)", r"\1", category_data).replace("'", '"')

                # Attempt to convert the cleaned string to a dictionary
                res = json.loads(clean_str)

                # Append the result to the current category's result list
                category_res.append(res)
            except json.JSONDecodeError as e:
                continue

        # Store the results of the current category in the all_res dictionary
        all_res[category_name] = category_res

    # Return the dictionary with all results
    return all_res


def transform_row(df):
    results = {}  # Initialize the results dictionary

    # Loop through each row in the DataFrame
    for i in range(len(df)):
        result = transform_data(df.iloc[i])
        results[f'row_{i}'] = result  # Store the result in the dictionary

    return results
