import streamlit as st
import psycopg2
import pandas as pd
from db import get_connection
from utils import spacing_placeholder

st.set_page_config(page_title="Data Viewer", page_icon="📊", layout="wide")

# --- Connect to DB ---
conn = get_connection()
cur = conn.cursor()

# --- Fetch data ---
cur.execute("SELECT * FROM union_member;")
data = cur.fetchall()
columns = [desc[0] for desc in cur.description]

# --- Convert to DataFrame ---
df = pd.DataFrame(data, columns=columns)

# --- Show all data ---
st.header("Union Members Data")
st.dataframe(df)

# --- Attendance count ---
if "attendance" in df.columns:
    total_attendance = df[df["attendance"] == "Yes"].shape[0]
    total_members = df.shape[0]

    st.markdown(f"***Total attendance: {total_attendance} / {total_members} orang***")

    if total_members > 0:
        percentage = (total_attendance / total_members) * 100
        st.markdown(f"***Percentage: {percentage:.2f}% hadir***")
else:
    st.warning("⚠️ Attendance column not found in database.")

spacing_placeholder(3)

# --- Staff Selector ---
staff_id_selector = st.selectbox("Select Staff", options=df['staff_id'].to_list())

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
        font-family: Arial, sans-serif;
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

cur.close()
conn.close()
