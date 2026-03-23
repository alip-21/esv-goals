import streamlit as st
import pandas as pd

st.markdown("""
    <style>
    /* 1. Target the 'Barrel' container specifically */
    div[data-testid="stAppViewBlockContainer"] {
        min-height: 100vh !important;
        height: auto !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* 2. Target the parent scroll container */
    div[data-testid="stAppViewContainer"] {
        height: 100vh !important;
    }

    /* 3. Remove the 'max-width' that Centered mode sometimes forces */
    .main .block-container {
        max-width: 95% !important;
    }

    /* 4. Force visibility on the bottom half */
    #root, .appview-container {
        height: 100vh !important;
        overflow: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)

def check_password():

    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Enter Password to Access ESV Goals", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Enter Password to Access ESV Goals", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():

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
