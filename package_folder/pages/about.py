import streamlit as st
import os

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .big-font {
        font-size:50px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .header-text {
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the header image
header_path = os.path.join(current_dir, "..", "frontend_data", "flatquest_header.jpg")
kiez_path = os.path.join(current_dir, "..", "frontend_data", "kiez.jpg")
schlange_path = os.path.join(current_dir, "..", "frontend_data", "schlange.jpg")
bezirk_path = os.path.join(current_dir, "..", "frontend_data", "bezirk.jpg")
map_path = os.path.join(current_dir, "..", "frontend_data", "cafe_map.png")
umziehen_path = os.path.join(current_dir, "..", "frontend_data", "umziehen.jpg")

# Display the header image
st.image(header_path, use_column_width=True)

# Applying the custom CSS class to your text
st.markdown('<p class="big-font">The Problem we are Solving</p>', unsafe_allow_html=True)

# Creating two columns
col1, spacer, col2 = st.columns([1, 0.2, 1])

# Adding content to the left column (col1)
with col1:
    st.markdown("### High Demand in Popular Areas")
    st.image(bezirk_path, caption="Rental prices per district")
    st.write("Popular neighborhoods are in high demand, leading to limited availability and inflated prices, forcing many to settle for less desirable options.")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("### Search platforms are not neighborhood-aware")
    st.image(map_path, caption="Screenshot of a popular rental platform")
    st.write("Popular search platforms don't allow users look for apartments close to ameneties that are important to them. This is equivalent to looking for the right apartment in the wrong place")



# Adding content to the right column (col2)
with col2:
    st.markdown("### Limited Neighborhood Knowledge")
    st.image(umziehen_path, caption="Berlin neighborhood")
    st.write("Many Berlin apartment hunters, especially newcomers, lack in-depth information about neighborhoods outside of popular areas like Kreuzberg and Prenzlauer Berg, making it difficult to explore other suitable options.")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("### Missed Opportunities in Lesser-Known Areas")
    st.image(kiez_path, caption="Berlin neighborhood")
    st.write("Without a way to filter and discover areas based on specific amenities or services, users might overlook neighborhoods that could be a perfect fit for their needs, simply because they are not as well-known or popular.")
