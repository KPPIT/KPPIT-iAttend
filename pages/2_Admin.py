import streamlit as st
import pandas as pd
from db import get_by_query
from pagar import main
from utils import spacing_placeholder

st.set_page_config(page_title="Admin | iAttend", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

if st.session_state.get("logged_in", False):

    # Fetch data from DB
    data, columns = get_by_query("SELECT * FROM union_member;")
    df = pd.DataFrame(data, columns=columns)

    # variable setup for visual summary setup
    total_attendance = df[df["attendance"] == "Yes"].shape[0]
    total_members = len(df)
    percentage_attendance = total_attendance / total_members * 100


    # --- Show all data ---
    st.header("Senarai Ahli Union")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Jumlah Kedatangan", value=total_attendance)
    col2.metric(label="Peratusan Attendance", value=f"{percentage_attendance:.2f}%")
    col3.metric(label="Jumlah Ahli", value=total_members)
    st.data_editor(df)

    spacing_placeholder(2)

    # --- Staff Selector ---
    staff_id_selector = st.selectbox("Staff ID: ", options=df['staff_id'].to_list())

    # Get the selected row
    staff_row = df[df['staff_id'] == staff_id_selector].iloc[0]

    # --- Decide card color based on attendance ---
    if staff_row['attendance'] == "Yes":
        card_color = "#2e7d32"  # Green
    else:
        card_color = "#4a4a4a"  # Grey

    # --- Display selected staff ---
    st.markdown(
        f"""
        <div style="
            padding:20px; 
            border-radius:15px; 
            background-color:{card_color};  
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
            margin-bottom:20px;
            font-family: Arial, serif;
            color: white;  
        ">
            <h3 style="margin-bottom:10px; color:white;">
                {staff_row['employee_name']}
            </h3>
            <p><strong>Staff ID:</strong> {staff_row['staff_id']}</p>
            <p><strong>Company:</strong> {staff_row['company_name']}</p>
            <p><strong>Unit:</strong> {staff_row['organizational_unit']}</p>
            <p><strong>Attendance:</strong> {staff_row['attendance'] if pd.notna(staff_row['attendance']) else "-"}</p>
            <p><strong>Check-in Time:</strong> {staff_row['checkin_time'] if pd.notna(staff_row['checkin_time']) else "-"}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Load login page
main ()