import streamlit as st
import pandas as pd
from db import get_by_query
from pagar import main
from utils import spacing_placeholder, load_css

# Call the function to load the CSS file
load_css("style.css")

st.set_page_config(
    page_title="Admin | iAttend",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def custom_table(header: str, dataframe):
    st.header(header)
    st.write(f"***Jumlah Carian: {len(dataframe)} ahli***")
    st.dataframe(
        dataframe,
        hide_index=True
    )

if st.session_state.get("logged_in", False):

    # Fetch data from DB
    data, columns = get_by_query("SELECT * FROM union_members;")
    df = pd.DataFrame(data, columns=columns)

    # Rename columns for better display
    df.rename(columns={
        'staff_id': 'Staff ID',
        'name': 'Nama',
        'attendance': 'Attendance',
        'checkin_time': 'Masa'
    }, inplace=True)

    # Always sort the dataframe by check-in time ascending
    df.sort_values(by=["Masa", "Staff ID"], ascending=[True, True], inplace=True)

    # --- Stats ---
    total_attendance = df[df["Attendance"] == "Yes"].shape[0]
    total_members = len(df)
    percentage_attendance = total_attendance / total_members * 100 if total_members > 0 else 0

    st.header("Senarai Ahli Kesatuan")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Jumlah Kedatangan", value=total_attendance)
    col2.metric(label="Peratusan Kedatangan", value=f"{percentage_attendance:.2f}%")
    col3.metric(label="Jumlah Ahli", value=total_members)

    with st.expander(label="Senarai Carian Penuh"):
        custom_table("Senarai Carian Penuh", df)
    
    # --- Search & Filter Section ---
    st.subheader("Carian Ahli")
    text_search = st.text_input("Carian Nama atau Staff ID", value="")

    # filter dataframe using masks
    m1 = df["Staff ID"].astype(str).str.contains(text_search)
    m2 = df["Nama"].astype(str).str.contains(text_search, case=False)
    df_search = df[m1 | m2 ] if text_search else df

    df_search_checkin = df_search[df_search["Attendance"] == "Yes"]
    df_search_non_checkin = df_search[df_search["Attendance"] != "Yes"]

    col1, col2 = st.columns(2)
    with col1:
        custom_table("Telah Daftar", df_search_checkin)

    with col2:
        custom_table("Belum Daftar", df_search_non_checkin)

# Load login page
main()
