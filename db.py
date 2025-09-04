import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(
        host=st.secrets["db"]["host"],
        dbname=st.secrets["db"]["dbname"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        port=st.secrets["db"]["port"]
    )

# Function to retrive staff data
def check_staff(staff_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT staff_id, employee_name, company_name, organizational_unit, attendance, checkin_time "
        "FROM union_member WHERE staff_id = %s", 
        (staff_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row