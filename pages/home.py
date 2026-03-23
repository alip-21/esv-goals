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

# 5. Podium
st.subheader("Podium")

ranking_metric = st.selectbox(
    "Rank Podium by:",
    options=["Success Rate", "Total Goals", "Total Shots"],
    index=0
)

metric_map = {
    "Success Rate": {"col": "Success_Rate", "format": ":.0%", "label": "Success Rate"},
    "Total Goals": {"col": "Total_Completed", "format": ":g", "label": "Goals Met"},
    "Total Shots": {"col": "Total_Shots", "format": ":g", "label": "Shots Taken"}
}

podium_df = (
    df.groupby("Person")
    .agg(
        Total_Goals=("Goal", "count")
        Total_Completed=("Complete", "sum"),
        Total_Shots=("Shot", "sum")    
    )
    .reset_index()
)

podium_df["Success_Rate"] = podium_df["Total_Completed"] / podium_df["Total_Goals"]

podium_df = podium_df.sort_values(by=selected["col"], ascending=False).reset_index(drop=True)

winners = podium_df.head(3).to_dict('records')

col2, col1, col3, list_col = st.columns([2,2,2,3])

with col1:
    with st.container(border=True, height=246):
        st.markdown(f"### 🥇 {winners[0]['Person']}")
        st.metric(selected["label"], f"{winners[0][selected['col']]{selected['format']}}")

with col2:
    st.write("")
    with st.container(border=True, height=230):
        st.markdown(f"### 🥈 {winners[1]['Person']}")
        st.metric(selected["label"], f"{winners[1][selected['col']]{selected['format']}}")

with col3:
    st.write("")
    st.write("")
    with st.container(border=True, height=214):
        st.markdown(f"### 🥉 {winners[2]['Person']}")
        st.metric(selected["label"], f"{winners[2][selected['col']]{selected['format']}}")

with list_col:
    st.subheader("🏃 ... and the Rest")
    rest_df = leaderboard_df.iloc[3:10][["Person", selected["col"]]]
    
    if not rest_df.empty:
        rest_df.columns = ["Name", selected["label"]]
        
        st.table(rest_df)
    else:
        st.write("No other data to display.")
