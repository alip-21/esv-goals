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

# 4. Page filters
latest_year = int(df["Year"].max())
df_historical = df[df["Year"] < latest_year]

# 5. 4 metrics across 4 columns
_, col1, col2, col3, col4, _ = st.columns([1,2,2,2,2,0.1])

total_goals = len(df_historical)
total_completed = df_historical["Complete"].sum()
total_shots = df_historical["Shot"].sum()

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

# 6. Podium
st.subheader("Podium")

ranking_metric = st.selectbox(
    "Rank Podium by:",
    options=["Success Rate", "Total Goals", "Total Shots"],
    index=0
)

metric_map = {
    "Success Rate": {"col": "Success_Rate", "format": "{:.0%}", "label": "Success Rate"},
    "Total Goals": {"col": "Total_Goals", "format": "{:g}", "label": "Total Goals"},
    "Total Shots": {"col": "Total_Shots", "format": "{:g}", "label": "Shots Taken"}
}
selected = metric_map[ranking_metric]

podium_df = (
    df_historical.groupby("Person")
    .agg(
        Total_Goals=("Goal", "count"),
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
    st.markdown("<h3 style='text-align: center;'>🥇</h3>", unsafe_allow_html=True)
    with st.container(border=True, height=246):
        st.markdown(f"**{winners[0]['Person']}**")
        val = winners[0][selected['col']]
        st.metric(selected["label"], selected["format"].format(val))

with col2:
    st.write("") 
    st.markdown("<h3 style='text-align: center;'>🥈</h3>", unsafe_allow_html=True)
    with st.container(border=True, height=230):
        st.markdown(f"**{winners[1]['Person']}**")
        val = winners[1][selected['col']]
        st.metric(selected["label"], selected["format"].format(val))

with col3:
    st.write("")
    st.write("")
    st.markdown("<h3 style='text-align: center;'>🥉</h3>", unsafe_allow_html=True)
    with st.container(border=True, height=214):
        st.markdown(f"**{winners[2]['Person']}**")
        val = winners[2][selected['col']]
        st.metric(selected["label"], selected["format"].format(val))

with list_col:
    st.subheader("🏃 ... and the Rest")
    rest_df = podium_df.iloc[3:10][["Person", selected["col"]]]
    
    if not rest_df.empty:
        rest_df.insert(0, "Rank", range(4, 4 + len(rest_df)))
        rest_df[selected["col"]] = rest_df[selected["col"]].map(selected["format"].format)
        rest_df.columns = ["Rank", "Name", selected["label"]]
        st.table(rest_df.set_index("Rank"))
    else:
        st.write("No other data to display.")
