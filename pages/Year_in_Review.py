import streamlit as st
import pandas as pd

# This "caches" the data so the app stays fast and doesn't ping Google Sheets every time you switch pages
@st.cache_data
def load_data():
    SHEET_ID = st.secrets["spreadsheet_id"].strip()
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    return pd.read_csv(url)

df = load_data()

# --- Page Specific Content ---
st.title("Year in Review")
st.write("This is where we celebrate the 100%ers.")
# Add your charts or specific "Hall of Fame" filters here...
