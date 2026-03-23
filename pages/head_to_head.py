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

# 4. Preparation: Get stats for every person
all_stats = (
    df.groupby("Person")
    .agg(
        Total_Goals=("Goal", "count"),
        Total_Completed=("Complete", "sum"),
        Total_Shots=("Shot", "sum")
    )
    .reset_index()
)
all_stats["Success_Rate"] = all_stats["Total_Completed"] / all_stats["Total_Goals"]

# 4. Selectors
people = sorted(all_stats["Person"].unique())

col_left, _, col_right = st.columns([4, 1, 4])

with col_left:
    p1_name = st.selectbox("Select Challenger 1", options=people, index=0)
    p1 = all_stats[all_stats["Person"] == p1_name].iloc[0]

with col_right:
    p2_name = st.selectbox("Select Challenger 2", options=people, index=1 if len(people) > 1 else 0)
    p2 = all_stats[all_stats["Person"] == p2_name].iloc[0]

st.markdown("---")

# 5. Comparison Logic Function
def compare_metric(label, val1, val2, is_pct=False):
    c1, c2, c3 = st.columns([4, 2, 4])
    
    # Formatting
    fmt = "{:.1%}" if is_pct else "{:g}"
    
    # Determine who wins this metric
    p1_win = "✅" if val1 > val2 else ""
    p2_win = "✅" if val2 > val1 else ""
    
    with c1:
        st.metric(label, fmt.format(val1), delta=p1_win if p1_win else None, delta_color="normal")
    with c2:
        st.markdown(f"<p style='text-align: center; padding-top: 25px; color: gray;'>VS</p>", unsafe_allow_html=True)
    with c3:
        st.metric(label, fmt.format(val2), delta=p2_win if p2_win else None, delta_color="normal")

  # 6. Display the Comparison Rows
compare_metric("Success Rate", p1["Success_Rate"], p2["Success_Rate"], is_pct=True)
compare_metric("Goals Completed", p1["Total_Completed"], p2["Total_Completed"])
compare_metric("Total Goals Set", p1["Total_Goals"], p2["Total_Goals"])
compare_metric("Total Shots", p1["Total_Shots"], p2["Total_Shots"])

# 7. Fun "Winner" Banner
st.markdown("---")
if p1["Success_Rate"] > p2["Success_Rate"]:
    st.success(f"🏆 Currently Leading: **{p1_name}**")
elif p2["Success_Rate"] > p1["Success_Rate"]:
    st.success(f"🏆 Currently Leading: **{p2_name}**")
else:
    st.info("🤝 It's a dead heat!")
