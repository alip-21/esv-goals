import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ESV Goals Tracker", layout="wide")

# 2. Connect to your Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Load Data
df = pd.read_csv(url)

# 3. Sidebar Filters
st.sidebar.header("Filter the Bloodbath")
selected_year = st.sidebar.multiselect("Select Year", options=df["Year"].unique(), default=df["Year"].unique())
selected_person = st.sidebar.multiselect("Select Person", options=df["Person"].unique(), default=df["Person"].unique())
selected_category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())

# Filter the data based on selection
filtered_df = df[(df["Year"].isin(selected_year)) & (df["Person"].isin(selected_person)) & (df["Category"].isin(selected_category))]

# --- 4. Main Dashboard ---
st.title("🏆 ESV Annual Goals & Penalty Shots")

# Create 3 columns
col1, col2, col3 = st.columns(3)

total_shots = filtered_df["Shot"].sum()
total_goals = len(filtered_df)
successes = len(filtered_df[filtered_df["Status"] == "Yes"])

# Metric 1: Total Goals
with col1:
    st.metric(label="Total Goals", value=total_goals)

# Metric 2: Total Shots
with col2:
    st.metric(label="Total Shots", value=int(total_shots))

# Metric 3: Success Rate
with col3:
    # Calculating %: (Count of 'Yes' / Total Goals) * 100
    if total_goals > 0:
        rate = (successes / total_goals) * 100
        st.metric(label="Success Rate", value=f"{rate:.1f}%")
    else:
        st.metric(label="Success Rate", value="0%")

st.divider() # Adds a nice clean line under your metrics

# Show the Data Table
st.subheader("Goal Details")
st.dataframe(filtered_df[["Year", "Person", "Goal", "Status", "Shot"]], use_container_width=True)

# 5. The "Hall of Shame" Chart
st.subheader("Penalty Shot Leaderboard")
shot_chart_data = filtered_df.groupby("Person")["Shot"].sum().sort_values(ascending=False)
st.bar_chart(shot_chart_data)
