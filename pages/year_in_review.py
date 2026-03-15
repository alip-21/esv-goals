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

winners = podium_df.to_dict('records')

col2, col1, col3 = st.columns(3)

with col1:
    with st.container(border=True, height=246):
        st.markdown(f"### 🥇 {winners[0]['Person']}")
        st.metric("Success Rate", f"{winners[0]['Success_Rate']:.0%}")
        st.caption(f"{int(winners[0]['Total_Goals'])} Total Goals")

with col2:
    st.write("")
    with st.container(border=True, height=230):
        st.markdown(f"### 🥈 {winners[1]['Person']}")
        st.metric("Success Rate", f"{winners[1]['Success_Rate']:.0%}")
        st.caption(f"{int(winners[1]['Total_Goals'])} Total Goals")

with col3:
    st.write("")
    st.write("")
    with st.container(border=True, height=214):
        st.markdown(f"### 🥉 {winners[2]['Person']}")
        st.metric("Success Rate", f"{winners[2]['Success_Rate']:.0%}")
        st.caption(f"{int(winners[2]['Total_Goals'])} Total Goals")

# 7. Chart - Success Rate

st.subheader("✅ Success Rate")

dimension = st.radio(
    "View Success Rate by:",
    options=["Person", "Category"],
    horizontal=True
)

success_rate_chart_data = (
    filtered_df.groupby(dimension)
    .agg(Total_Shots=("Shot","sum"), Total_Goals=("Goal", "count"))
    .reset_index()
)

success_rate_chart_data["Success_Rate"] = (
    (success_rate_chart_data["Total_Goals"] - success_rate_chart_data["Total_Shots"]) 
    / success_rate_chart_data["Total_Goals"]
)

success_rate_chart_data = success_rate_chart_data.sort_values(
    by=["Success_Rate", "Total_Goals"], 
    ascending=[False, False]
)

chart = (
    alt.Chart(success_rate_chart_data)
    .mark_bar()
    .encode(
        x=alt.X(f"{dimension}:N", sort="-y", title=dimension, axis=alt.Axis(labelAngle=45)), 
        y=alt.Y("Success_Rate:Q", title="Success Rate", axis=alt.Axis(format='%')),
        color=alt.value("#1c1f3e"),
        tooltip=[
            alt.Tooltip(f"{dimension}", title=dimension),
            alt.Tooltip("Success_Rate", format=".0%", title="Success Rate"),
            alt.Tooltip("Total_Goals", title="Total Goals"),
            alt.Tooltip("Total_Shots", title="Total Shots"),
        ]
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)


# 8. Chart = Total shots
st.subheader("🥃 Shots")

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
