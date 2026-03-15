import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="ESV Goals Database", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Page header
st.title("ESV Goals Database")

# 4. Page filters
with st.expander("🔍", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_year = st.multiselect(
            "Select Year", 
            options=sorted(df["Year"].unique()), 
            default=df["Year"].unique()
        )
    
    with col2:
        selected_person = st.multiselect(
            "Select Person", 
            options=sorted(df["Person"].unique()),
            default=df["Person"].unique()
        )
        
    with col3:
        selected_category = st.multiselect(
            "Select Category", 
            options=sorted(df["Category"].unique()),
            default=df["Category"].unique()
        )

filtered_df = df[(df["Year"].isin(selected_year)) & (df["Person"].isin(selected_person)) & (df["Category"].isin(selected_category))]

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
