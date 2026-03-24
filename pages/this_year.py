import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="This Year", layout="wide")

# 2. Connect to Google Sheet (Export to CSV link)
SHEET_ID = st.secrets["spreadsheet_id"]
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
df = pd.read_csv(url)

# 3. Filter for the current year only
current_year = df["Year"].max()
current_goals = df[df["Year"] == current_year].copy()

# 4. Page header
st.title(f"🎯 {current_year} Goals")

# 5. Pivot the data
cat_mapping = (
    df[["Category ID", "Category"]]
    .drop_duplicates()
    .sort_values("Category ID")
)
sorted_category_names = cat_mapping["Category"].tolist()

pivot_df = (
    current_goals.groupby(["Person", "Category"])["Goal"]
    .apply(lambda x: "<br>• " + "<br>• ".join(x))
    .unstack(fill_value="-")
)

# 6. Custom CSS to make the table look like a "Grid"
st.markdown("""
    <style>
    .goals-grid {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        font-size: 0.85rem;
    }
    .goals-grid th {
        background-color: #1c1f3e;
        color: white;
        padding: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }
    .goals-grid td {
        padding: 10px;
        border: 1px solid #ddd;
        vertical-align: top;
        line-height: 1.4;
    }
    .goals-grid tr:nth-child(even) {background-color: #f9f9f9;}
    </style>
""", unsafe_allow_html=True)

# 7. Convert the DataFrame to HTML and display
# 'escape=False' is critical so the <br> tags actually create new lines
html_table = pivot_df.to_html(escape=False, classes='goals-grid')
st.markdown(html_table, unsafe_allow_html=True)
