import streamlit as st
import pandas as pd
import altair as alt

# 1. Page configuration
st.set_page_config(page_title="Head to Head", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Page header
st.title("Head to Head")

# 3. Page filter

with st.expander("🎯 Filter by Category", expanded=False):
    latest_year = int(df["Year"].max())
    df_historical = df[df["Year"] < latest_year]
    
    categories = ["All"] + sorted(df["Category"].unique().tolist())
    selected_cat = st.selectbox("Select Category Focus", options=categories)

if selected_cat != "All":
    display_df = df_historical[df_historical["Category"] == selected_cat]
else:
    display_df = df_historical

# 4. Preparation: Get stats for every person
all_stats = (
    display_df.groupby("Person")
    .agg(
        Total_Goals=("Goal", "count"),
        Total_Completed=("Complete", "sum"),
        Total_Shots=("Shot", "sum")
    )
    .reset_index()
)
all_stats["Success_Rate"] = all_stats["Total_Completed"] / all_stats["Total_Goals"]

# 5. Selectors
people = sorted(all_stats["Person"].unique())

col_left, _, col_right = st.columns([4, 1, 4])

with col_left:
    p1_name = st.selectbox("Select Challenger 1", options=people, index=0)
    p1 = all_stats[all_stats["Person"] == p1_name].iloc[0]

with col_right:
    p2_name = st.selectbox("Select Challenger 2", options=people, index=1 if len(people) > 1 else 0)
    p2 = all_stats[all_stats["Person"] == p2_name].iloc[0]

st.markdown("---")

# 6. Comparison Logic Function
def compare_metric(label, val1, val2, is_pct=False, lower_is_better=False):
    c1, c2, c3 = st.columns([4, 1, 4])

    fmt = "{:.1%}" if is_pct else "{:g}"
    v1_str = fmt.format(val1)
    v2_str = fmt.format(val2)

    if lower_is_better:
        p1_wins = val1 < val2
        p2_wins = val2 < val1
    else:
        p1_wins = val1 > val2
        p2_wins = val2 > val1

    win_style = "color: #1B8532; font-size: 24px; font-weight: bold;"
    lose_style = "color: #6c757d; font-size: 24px;"

    with c1:
        st.markdown(f"<p style='text-align: right; margin-bottom: -10px; color: gray; font-size: 14px;'>{label}</p>", unsafe_allow_html=True)
        style = win_style if p1_wins else lose_style
        st.markdown(f"<p style='{style} text-align: right;'>{v1_str}</p>", unsafe_allow_html=True)

    with c2:
        st.markdown("<p style='text-align: center; color: #ced4da; margin-top: 25px; font-weight: bold;'>VS</p>", unsafe_allow_html=True)
    with c3:
        st.markdown(f" <p style='text-align: left; margin-bottom: -10px; color: gray; font-size: 14px;'>{label}</p>", unsafe_allow_html=True)
        style = win_style if p2_wins else lose_style
        st.markdown(f"<p style='{style} text-align: left;'>{v2_str}</p>", unsafe_allow_html=True)

# 7. Display the Comparison Rows
compare_metric("Success Rate", p1["Success_Rate"], p2["Success_Rate"], is_pct=True)
compare_metric("Goals Completed", p1["Total_Completed"], p2["Total_Completed"])
compare_metric("Total Goals", p1["Total_Goals"], p2["Total_Goals"])
compare_metric("Total Shots", p1["Total_Shots"], p2["Total_Shots"], lower_is_better=True)
