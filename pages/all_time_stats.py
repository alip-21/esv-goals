import streamlit as st
import pandas as pd
import altair as alt

# 1. Page configuration
st.set_page_config(page_title="All Time Stats", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Page header
st.title("All Time Stats")

# 4. Page filters
with st.expander("🔍", expanded=False):

    latest_year = int(df["Year"].max())
    df_historical = df[df["Year"] < latest_year]
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_person = st.multiselect(
            "Select Person", 
            options=sorted(df["Person"].unique()),
            default=df["Person"].unique()
        )
        
    with col2:
        selected_category = st.multiselect(
            "Select Category", 
            options=sorted(df["Category"].unique()),
            default=df["Category"].unique()
        )

filtered_df = df_historical[
    (df_historical["Person"].isin(selected_person)) & 
    (df_historical["Category"].isin(selected_category))
]

st.markdown("")

# 5. 4 metrics across 6 columns
_, col1, col2, col3, col4, _ = st.columns([1,2,2,2,2,0.1])

total_goals = len(filtered_df)
total_completed = filtered_df["Complete"].sum()
total_shots = filtered_df["Shot"].sum()

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

# 6. Chart - Success Rate

st.subheader("✅ Success Rate")

dimension_success = st.radio(
    "View Success Rate by:",
    options=["Person", "Category"],
    horizontal=True
)

if dimension_success == "Category":
    angle = -45
else:
    angle = 0

success_rate_chart_data = (
    filtered_df.groupby(dimension_success)
    .agg(Total_Completed=("Complete","sum"), Total_Goals=("Goal", "count"))
    .reset_index()
)

success_rate_chart_data["Success_Rate"] = (
    success_rate_chart_data["Total_Completed"] / success_rate_chart_data["Total_Goals"]
)

success_rate_chart_data = success_rate_chart_data.sort_values(
    by=["Success_Rate", "Total_Goals"], 
    ascending=[False, False]
)

chart = (
    alt.Chart(success_rate_chart_data)
    .mark_bar()
    .encode(
        x=alt.X(f"{dimension_success}:N", sort="-y", title=dimension_success, axis=alt.Axis(labelAngle=angle)), 
        y=alt.Y("Success_Rate:Q", title="Success Rate", axis=alt.Axis(format='%')),
        color=alt.value("#1c1f3e"),
        tooltip=[
            alt.Tooltip(f"{dimension_success}", title=dimension_success),
            alt.Tooltip("Success_Rate", format=".0%", title="Success Rate"),
            alt.Tooltip("Total_Goals", title="Total Goals"),
            alt.Tooltip("Total_Completed", title="Total Completed"),
        ]
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)

# 7. Chart = Total shots
st.subheader("🥃 Shots")

dimension_shots = st.radio(
    "View Shots by:",
    options=["Person", "Category"],
    horizontal=True
)

if dimension_shots == "Category":
    angle = -45
else:
    angle = 0

shot_chart_data = (
    filtered_df.groupby(dimension_shots)
    .agg(Total_Shots=("Shot","sum"), Total_Goals=("Goal", "count"))
    .reset_index()
    .sort_values(by=["Total_Shots", "Total_Goals"], ascending=[False, True])
)

chart = (
    alt.Chart(shot_chart_data)
    .mark_bar()
    .encode(
        x=alt.X(f"{dimension_shots}:N", sort="-y", title=dimension_shots, axis=alt.Axis(labelAngle=angle)), 
        y=alt.Y("Total_Shots:Q", title="Shots"),
        color=alt.value("#1c1f3e")
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)

# 8. Chart = Evolution
st.subheader("📈 Evolution")

dimension_trend = st.radio(
    "Break out Trend by:",
    options=["Person", "Category"],
    horizontal=True,
    key="trend_dimension_toggle"
)

metric_trend = st.radio(
    "Select Metric:",
    options=["Success Rate", "Total Goals", "Total Shots"],
    horizontal=True,
    key="trend_metric_toggle"
)

selection = alt.selection_point(fields=[dimension_trend], bind='legend')

trend_metric_map = {
    "Success Rate": {"col": "Success_Rate", "title": "Success Rate", "fmt": "%", "tip": ".0%"},
    "Total Goals": {"col": "Total_Goals", "title": "Total Goals Set", "fmt": "d", "tip": "d"},
    "Total Shots": {"col": "Total_Shots", "title": "Total Shots", "fmt": "d", "tip": "g"}
}
m_info = trend_metric_map[metric_trend]

trend_data = (
    filtered_df.groupby(["Year", dimension_trend])
    .agg(
        Total_Goals=("Goal", "count"), 
        Total_Completed=("Complete", "sum"),
        Total_Shots=("Shot", "sum")
    )
    .reset_index()
)

trend_data["Success_Rate"] = (
    trend_data["Total_Completed"] / trend_data["Total_Goals"].replace(0, 1)
)
  
chart = (
    alt.Chart(trend_data)
    .mark_line(point=True)
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y(f"{m_info['col']}:Q", title=m_info['title'], axis=alt.Axis(format=m_info['fmt'])),
        color=alt.condition(
            selection, 
            alt.Color(f"{dimension_trend}:N", title=dimension_trend), 
            alt.value("lightgray")
        ),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=[
            alt.Tooltip("Year"),
            alt.Tooltip(f"{dimension_trend}:N"),
            alt.Tooltip(f"{m_info['col']}:Q", format=m_info['tip'], title=m_info['title']),
            alt.Tooltip("Total_Goals:Q", title="Total Goals Set")
        ]
    )
    .add_params(selection)
    .properties(height=400)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)
