import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="ESV Goals Tracker", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Page header
st.title("🏆 ESV Goals")

# 4. 4 metrics across 4 columns
_, col1, col2, col3, col4, _ = st.columns([1,2,2,2,2,0.1])

total_goals = len(df)
total_completed = df["Complete"].sum()
total_shots = df["Shot"].sum()

# Metric 1: Total Goals
with col1:
    st.metric(label="Total Goals", value=total_goals)

# Metric 2: Total Shots
with col2:
    st.metric(label="Total Completed", value=total_completed)

# Metric 3: Success Rate
with col3:
    if total_goals > 0:
        rate = (total_completed / total_goals) * 100
        st.metric(label="Success Rate", value=f"{rate:.1f}%")
    else:
        st.metric(label="Success Rate", value="0%")

# Metric 4: Total Shots
with col4:
    st.metric(label="Total Shots", value=total_shots)

st.markdown("")
