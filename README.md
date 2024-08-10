![Subdirectory Image](./package_folder/frontend_data/flatquest_header.jpg)
# Flatquest App

This Streamlit app helps users find apartments based on their preferences and
visualizes points of interest around selected addresses using Folium maps.

## Features

- Input fields for total rent, living space, number of rooms, and balcony
preference
- Selection of up to three categories of interest (e.g., restaurant, bar, gym)
- Visualization of selected apartments and nearby points of interest on an
interactive map

## Installation

To run this app locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/apartment-finder-app.git
   cd apartment-finder-app

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt

4. **Run the App:**

   ```bash
   streamlit run home.py


## How to Use
 - Open the app: Once you run the app with streamlit run main_script.py, it will
  open in your default web browser.
 - Enter your preferences: Fill in the desired total rent, living space, number
 of rooms, and balcony preference.
 - Select points of interest: Choose up to three categories of interest from the
  options provided.
 - Submit: Click the "Submit" button to see the results.
 - View results: The app will display a map with the selected apartments and
 nearby points of interest.

## Deployment
To deploy this app on Streamlit Cloud:
- Push your code to a GitHub repository.
- Go to Streamlit Cloud and sign in.
- Click on "New app" and connect your GitHub repository.
- Follow the instructions to deploy the app.

## Troubleshooting
If the app cannot locate the berlin_cleaned.csv file during deployment, ensure
that:

- The file is included in your GitHub repository.
- The path to the file in home.py is correct.
