import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="Year in Review", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Page header
st.title("Year in Review")

# 4. Page filters
with st.expander("🔍", expanded=False):
    selected_year = st.multiselect(
        "Select Year",             
        options=sorted(df["Year"].unique()), 
        default=df["Year"].unique()
    )
    
filtered_df = df[(df["Year"].isin(selected_year))]

# 5. Data table
dynamic_height = min(600, (len(filtered_df)*35)+45)
st.dataframe(
    filtered_df[["Year", "Person", "Category", "Goal", "Status", "Shot"]],
    use_container_width=True,
    hide_index=True,
    height=dynamic_height,
    column_config={
        "Year": st.column_config.TextColumn("Year"),
        "Shot": st.column_config.TextColumn("Shot"),
    }
)
