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

def draw_podium_col(column, winner, rank_emoji, rank_num, height_offset):
    with column:
        for _ in range(height_offset):
            st.write("")            
        with st.container(border=True, height=220):
            st.markdown(f"### {rank_emoji} {rank_num} {winner['Person']}")
            st.metric("Success Rate", f"{winner['Success_Rate']:.0%}")
            st.caption(f"{int(winner['Total_Goals'])} Total Goals")

    draw_podium_col(col2, winners[1], "🥈", "#2", 2) # Offset by 2 for Silver
    draw_podium_col(col1, winners[0], "🥇", "#1", 0) # No offset for Gold
    draw_podium_col(col3, winners[2], "🥉", "#3", 4) # Offset by 4 for Bronze

else:
    st.warning("No data found for the current year")

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
