import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title = '2. About',
    layout = 'wide'
)

st.title("About")

st.markdown('''- **Limited Neighborhood Knowledge:** When searching for apartments in
            Berlin, users often lack comprehensive information about various
            neighborhoods, beyond the well-known areas like Kreuzberg,
            Friedrichshain, and Prenzlauer Berg. This makes it difficult for
            them to explore other potentially suitable areas that might meet
            their lifestyle needs.''')
st.markdown('''- **High Demand in Popular Areas:** The high
            demand for apartments in these trendy neighborhoods makes it
            challenging to find available and affordable housing, leaving users
            frustrated and often settling for less desirable options.''')
st.markdown('''- **Lack of Personalized Search Tools:** Traditional rental
            platforms focus mainly on basic criteria like price, size, and the
            number of bedrooms. They do not offer tools that allow users to
            search based on personal lifestyle preferences, such as proximity to
            gyms, public transportation, restaurants, parks, and schools.''')
st.markdown('''- **Missed Opportunities in Lesser-Known Areas:** Without a way to
            filter and discover areas based on specific amenities or services,
            users might overlook neighborhoods that could be a perfect fit for
            their needs, simply because they are not as well-known or popular.
            [Discover your new Kiez]''')
