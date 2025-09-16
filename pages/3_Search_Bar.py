import streamlit as st
import pandas as pd
from db import get_by_query
from pagar import main

st.set_page_config(page_title="Search Bar", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

def custom_table(header: str, dataframe):
    st.header(header)
    st.write(f"***Jumlah Carian: {len(dataframe)} ahli***")
    st.dataframe(
        dataframe,
        column_config={
            "company_name": None
        },
        hide_index=True
    )

if st.session_state.get("logged_in", False):
    st.title("Search Bar")

    data, columns = get_by_query("SELECT * FROM union_member;")
    df = pd.DataFrame(data, columns=columns)

    text_search = st.text_input("Carian Nama atau Staff ID atau Department", value="")
    button_search = st.button("search")

    # filter dataframe using masks
    m1 = df["staff_id"].astype(str).str.contains(text_search)
    m2 = df["employee_name"].astype(str).str.contains(text_search, case=False)
    m3 = df["organizational_unit"].astype(str).str.contains(text_search, case=False)
    df_search = df[m1 | m2 | m3]

    df_search_checkin = df_search[df_search["attendance"] == "Yes"]
    df_search_non_checkin = df_search[df_search["attendance"] != "Yes"]

    # show the results based on text_search
    if text_search is None:
        st.dataframe(df)

    else:
        col1, col2 = st.columns(2)

        with col1:
            custom_table("Telah Cek In", df_search_checkin)

        with col2:
            custom_table("Belum Daftar", df_search_non_checkin)

        with st.expander(label="Senarai Carian Penuh"):
            custom_table("Senarai Carian Penuh", df_search)

# login page
main ()