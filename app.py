import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ESV Goals Tracker", layout="wide")

# 2. Connect to your Google Sheet (Export to CSV link)
SHEET_ID = '1g5sGDtylfkkaoHjHlP_LXhZE7qo8NkqGagSGqzKg_iw'.strip()
SHEET_NAME = 'ESV Goals'.strip()
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Load Data
df = pd.read_csv(url)

# 3. Sidebar Filters
st.sidebar.header("Filter the Bloodbath")
selected_year = st.sidebar.multiselect("Select Year", options=df["Year"].unique(), default=df["Year"].unique())
selected_person = st.sidebar.multiselect("Select Person", options=df["Person"].unique(), default=df["Person"].unique())

# Filter the data based on selection
filtered_df = df[(df["Year"].isin(selected_year)) & (df["Person"].isin(selected_person))]

# 4. Main Dashboard
st.title("🥃 ESV Goals")

# Metric Row
total_shots = filtered_df["Shot"].sum()
st.metric(label="Total Shots Owed", value=int(total_shots))

# Show the Data Table
st.subheader("Goal Details")
st.dataframe(filtered_df[["Year", "Person", "Goal", "Status", "Shot"]], use_container_width=True)

# 5. The "Hall of Shame" Chart
st.subheader("Penalty Shot Leaderboard")
shot_chart_data = filtered_df.groupby("Person")["Shot"].sum().sort_values(ascending=False)
st.bar_chart(shot_chart_data)
