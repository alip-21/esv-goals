import streamlit as st
import pandas as pd
import altair as alt

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
st.subheader("Podium")

podium_df = (
    filtered_df.groupby("Person")
    .agg(Total_Goals=("Goal", "count"), Total_Shots=("Shot", "sum"))
    .reset_index()
)

podium_df["Success_Rate"] = (podium_df["Total_Goals"] - podium_df["Total_Shots"]) / podium_df["Total_Goals"]

podium_df = podium_df.sort_values(
    by=["Success_Rate", "Total_Goals"], 
    ascending=[False, False]
).head(3)

first = podium_df.iloc[0]
second = podium_df.iloc[1]
third = podium_df.iloc[2]

st.markdown("""
<style>
    .podium-box {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
    }
    .gold { background-color: #FFD700; color: black; margin-top: 0px; }
    .silver { background-color: #C0C0C0; color: black; margin-top: 40px; }
    .bronze { background-color: #CD7F32; color: black; margin-top: 80px; }
</style>
""", unsafe_allow_code=True)

col_2, col_1, col_3 = st.columns(3)

with col_2:
    st.markdown(f"""<div class='podium-box silver'>
        <h2>🥈</h2>
        <p>{second['Person']}</p>
        <h3>{second['Success_Rate']:.0%}</h3>
        <small>{second['Total_Goals']} Goals</small>
    </div>""", unsafe_allow_code=True)

with col_1:
    st.markdown(f"""<div class='podium-box gold'>
        <h2>🥇</h2>
        <p>{first['Person']}</p>
        <h3>{first['Success_Rate']:.0%}</h3>
        <small>{first['Total_Goals']} Goals</small>
    </div>""", unsafe_allow_code=True)

with col_3:
    st.markdown(f"""<div class='podium-box bronze'>
        <h2>🥉</h2>
        <p>{third['Person']}</p>
        <h3>{third['Success_Rate']:.0%}</h3>
        <small>{third['Total_Goals']} Goals</small>
    </div>""", unsafe_allow_code=True)

# 7. Chart = Total shots
st.subheader("Shots")

shot_chart_data = (
    filtered_df.groupby("Person")
    .agg(Total_Shots=("Shot","sum"), Total_Goals=("Goal", "count"))
    .reset_index()
    .sort_values(by=["Total_Shots", "Total_Goals"], ascending=[False, True])
)

chart = (
    alt.Chart(shot_chart_data)
    .mark_bar()
    .encode(
        x=alt.X("Person:N", sort="-y", title="Person"), 
        y=alt.Y("Total_Shots:Q", title="Shots"),
        color=alt.value("#1c1f3e")
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)
