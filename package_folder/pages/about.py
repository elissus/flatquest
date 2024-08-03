import streamlit as st
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the header image
relative_path = os.path.join("..", "frontend_data", "flatquest_header.jpg")

# Construct the absolute path
image_path = os.path.join(current_dir, relative_path)


# Display the header image
st.image(image_path, use_column_width=True)

# About page content
about_text = """

Once upon a time, in a land not so far away, there was a valiant hero—you—on a grand quest. This wasn’t just any quest; it was the ultimate adventure of finding the perfect apartment. In the vast kingdom of real estate, filled with dragons of high rent and dungeons of tiny living spaces, you needed more than just courage. You needed FlatQuest!

FlatQuest is not your ordinary real estate app; it's your enchanted map, guiding you through the treacherous terrain of apartment hunting. As you don your armor and set out on this noble journey, FlatQuest ensures that you find a dwelling that meets all your heroic needs—not just in size but also in the magical infrastructure surrounding it.

Imagine a scroll that not only lists apartments with ample living space and the perfect number of rooms but also marks the proximity to crucial landmarks. Need a tavern for nightly feasts? FlatQuest knows the best spots. Seeking schools for young apprentices? We’ve got you covered. Craving a park for your trusty steed (or perhaps a dog)? FlatQuest shows you the greenest pastures. Want a bustling marketplace of restaurants and bars for epic tales and merry-making? Your quest just got easier.

So, brave adventurer, strap on your boots, grab your wizard’s staff (or smartphone), and embark on this epic journey with FlatQuest. Because every hero deserves a happy ending in the perfect home. Onward to your next great adventure—your perfect flat awaits!
"""

# Streamlit app
st.title("Welcome to FlatQuest: Your Epic Journey to the Perfect Apartment!")
st.write(about_text)
