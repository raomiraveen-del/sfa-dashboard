import streamlit as st
import json
import os
import pandas as pd
import math

# --- Page setup ---
st.set_page_config(page_title="SFA Full Scraper", layout="wide")
st.title("Singapore Food Agency - Full Site Scraper")

# --- Load data ---
if not os.path.exists("sfa_full_output.json"):
    st.error("❌ No crawl data found. Please run SFAWebScraper.py first.")
else:
    with open("sfa_full_output.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Last crawl date ---
    if data:
        st.markdown(f"**Last Crawl Date:** {data[0].get('last_updated','N/A')}")

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Exports"])

    # --- Overview tab with charts ---
    with tab1:
        df = pd.DataFrame(data)
        st.subheader("Overview Charts")

        # Chart 1: Pages by depth
        if "depth" in df.columns:
            depth_counts = df["depth"].value_counts().sort_index()
            st.write("📊 Pages by Crawl Depth")
            st.bar_chart(depth_counts)

        # Chart 2: Pages by last_updated (grouped by date only)
        if "last_updated" in df.columns:
            df["last_updated_date"] = pd.to_datetime(df["last_updated"]).dt.date
            date_counts = df["last_updated_date"].value_counts().sort_index()
            st.write("📈 Pages Crawled per Date")
            st.line_chart(date_counts)

    # --- Details tab with search + pagination ---
    with tab2:
        search_term = st.text_input("Search keyword...", "").lower()
        filtered_data = [
            page for page in data
            if not search_term or search_term in page["content"].lower()
        ]

        rows_per_page = 50
        total_pages = max(1, math.ceil(len(filtered_data) / rows_per_page))
        page_number = st.number_input(
            "Page number", min_value=1, max_value=total_pages, value=1, step=1
        )

        start_index = (page_number - 1) * rows_per_page
        end_index = start_index + rows_per_page
        page_data = filtered_data[start_index:end_index]

        for page in page_data:
            with st.expander(page["url"], expanded=False):
                st.write(f"**Last Updated:** {page['last_updated']}")
                st.write(f"**Depth:** {page['depth']}")
                st.text(page["content"])

        st.write(f"Showing page {page_number} of {total_pages}")

    # --- Exports tab ---
    with tab3:
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
        csv_data = pd.DataFrame(data).to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="sfa_full_output.csv",
            mime="text/csv"
        )

        # Excel export
        excel_file = "sfa_full_output.xlsx"
        pd.DataFrame(data).to_excel(excel_file, index=False, engine="xlsxwriter")
        with open(excel_file, "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name="sfa_full_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
