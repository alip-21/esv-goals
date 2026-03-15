import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(layout="wide")

# Define the pages
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
year_in_review_page = st.Page("pages/year_in_review.py", title="Year in Review", icon="🗓️")

# Create navigation
pg = st.navigation(
    {"Menu":[home_page, year_in_review_page]},
    position="top"
)
pg.run()
