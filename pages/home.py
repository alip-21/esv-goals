import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="ESV Goals Tracker", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Page filters
with st.expander("🔍 Filter the Bloodbath", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_year = st.multiselect(
            "Select Year", 
            options=sorted(df["Year"].unique(), reverse=True), 
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

# 4. Page header
st.title("🏆 ESV Goals")

# 5. 3 metrics across 3 columns
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

# 6. Data table
st.subheader("Goal Details")
st.dataframe(
    filtered_df[["Year", "Person", "Goal", "Status", "Shot"]],
    use_container_width=True,
    hide_index=True
)

# 7. The "Hall of Shame" Chart
st.subheader("Penalty Shot Leaderboard")
shot_chart_data = filtered_df.groupby("Person")["Shot"].sum().sort_values(ascending=False)
st.bar_chart(shot_chart_data)
