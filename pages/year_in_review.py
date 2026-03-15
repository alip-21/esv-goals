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
unique_years = sorted(df["Year"].unique(), reverse=True)
default_year = 1

selected_year = st.selectbox(
    "Select Year",             
    options=unique_years, 
    index=default_year
)
    
filtered_df = df[df["Year"] == selected_year]

st.markdown("")

# 5. 3 metrics across 3 columns
_, col1, col2, col3, col4, _ = st.columns([1,2,2,2,2,0.1])

total_goals = len(filtered_df)
total_completed = filtered_df["Complete"].sum()
successes = len(filtered_df[filtered_df["Status"] == "Yes"])
total_shots = filtered_df["Shot"].sum()

# Metric 1: Total Goals
with col1:
    st.metric(label="Total Goals", value=total_goals)

# Metric 2: Total Shots
with col2:
    st.metric(label="Total Completed", value=int(total_completed))

# Metric 3: Success Rate
with col3:
    # Calculating %: (Count of 'Yes' / Total Goals) * 100
    if total_goals > 0:
        rate = (successes / total_goals) * 100
        st.metric(label="Success Rate", value=f"{rate:.1f}%")
    else:
        st.metric(label="Success Rate", value="0%")

# Metric 4: Total Shots
with col4:
    st.metric(label="Total Shots", value=int(total_shots))

st.markdown("")

# 6. Podium

# 7. The "Hall of Shame" Chart
st.subheader("Shots")
shot_chart_data = (
    filtered_df.groupby("Person")["Shot"]
    .sum()
    .reset_index()
    .sort_values(by="Shot", ascending=False))
st.bar_chart(shot_chart_data)
