import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SFA Full Scraper", layout="wide")
st.title("Singapore Food Agency - Full Site Scraper")

if not os.path.exists("sfa_full_output.json"):
    st.error("❌ No crawl data found. Please run SFAWebScraper.py first.")
else:
    with open("sfa_full_output.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    search_term = st.text_input("Search keyword...", "").lower()

    for page in data:
        if search_term and search_term not in page["content"].lower():
            continue

        with st.expander(page["url"], expanded=False):
            st.write(f"**Last Updated:** {page['last_updated']}")
            st.write(f"**Depth:** {page['depth']}")
            st.text(page["content"])

    # --- Export buttons ---
    st.subheader("Export Data")

    # JSON export
    download_json = json.dumps(data, indent=2)
    st.download_button(
        label="Download JSON",
        data=download_json,
        file_name="sfa_full_output.json",
        mime="application/json"
    )

    # CSV export
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="sfa_full_output.csv",
        mime="text/csv"
    )
