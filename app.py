import streamlit as st
from companies_client import search_companies, get_officers

st.set_page_config("Company Info Lookup", layout="wide")
st.title("🏢 Companies House Explorer")

company_name = st.text_input("🔍 Search for a company", placeholder="e.g. Vodafone")

if company_name:
    df = search_companies(company_name)

    if df.empty:
        st.warning("No companies found.")
    else:
        st.subheader("📦 Matching Companies")
        st.dataframe(df, use_container_width=True)

        index = st.selectbox(
            "Select a company by index",
            df.index,
            format_func=lambda i: f"{df.at[i, 'Company Name']} ({df.at[i, 'Company Number']})"
        )

        company_no = df.at[index, "Company Number"]
        st.write(f"🔍 Fetching officers for: `{df.at[index, 'Company Name']}`")

        officers_df = get_officers(company_no)

        st.subheader("👥 Officers")
        if not officers_df.empty:
            st.dataframe(officers_df, use_container_width=True)
        else:
            st.info("No officer data found.")