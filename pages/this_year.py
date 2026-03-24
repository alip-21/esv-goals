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

# 5. Sort by category ID and pivot the data
cat_mapping = (
    df[["Category ID", "Category"]]
    .drop_duplicates()
    .sort_values("Category ID")
)
sorted_category_names = cat_mapping["Category"].tolist()

pivot_df = (
    current_goals.groupby(["Person", "Category"])["Goal"]
    .apply(lambda x: "<div style='margin:0; padding:0;'>• " + "</div><div style='margin:0; padding:0;'>• ".join(x) + "</div>")
    .unstack(fill_value="<div style='color:#ccc;'>-</div>")
)

pivot_df.columns.name = None
pivot_df.index.name = None

existing_columns = [c for c in sorted_category_names if c in pivot_df.columns]
pivot_df = pivot_df[existing_columns]

# 6. Custom CSS to make the table look like a "Grid"
st.markdown("""
    <style>
    .goals-grid {
        width: 100%;
        border-collapse: collapse;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 0.82rem;
        table-layout: fixed; /* Keeps columns even on mobile */
    }
    
    .goals-grid th {
        background-color: #1c1f3e;
        color: white;
        padding: 4px 8px;
        border: 1px solid #ddd;
        text-align: center;
        vertical-align: middle;
        font-weight: 600;
    }
    
    .goals-grid td {
        padding: 4px 8px !important; /* Reduced vertical padding */
        border: 1px solid #ddd;
        vertical-align: middle !important;
        line-height: 1.1 !important;
        word-wrap: break-word;
    }

    /* Force the div inside the cell to have zero top margin */
    .goals-grid td div {
        margin: 0 !important;
        padding: 2px 0 !important; /* Tiny gap between goals, but none at the very top */
        display: block;
    }

    .goals-grid tr:nth-child(even) {background-color: #fcfcfc;}
    
    /* Makes the table scrollable on small screens */
    .table-container {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    </style>
""", unsafe_allow_html=True)

# 7. Convert the DataFrame to HTML and display
st.markdown(f'<div class="table-container">{pivot_df.to_html(escape=False, classes="goals-grid")}</div>', unsafe_allow_html=True)
