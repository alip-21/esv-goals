import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(layout="wide")

# Define the pages
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
year_in_review_page = st.Page("pages/year_in_review.py", title="Year in Review", icon="🗓️")
all_time_stats_page = st.Page("pages/all_time_stats.py", title="All Time Stats", icon="📈")
head_to_head_page = st.Page("pages/head_to_head.py", title="Head to Head", icon="🥊")
database_page = st.Page("pages/database.py", title="Goals Database", icon="💾")

# Create navigation
pg = st.navigation(
    {"Menu":[home_page, year_in_review_page, all_time_stats_page, head_to_head_page, database_page]},
    position="top"
)
pg.run()
