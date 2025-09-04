import streamlit as st
from datetime import datetime
from utils import gap
from db import get_connection  

st.set_page_config(page_title="Pengesahan", page_icon="📄", layout="centered")

# Retrieve data from session_state
staff_id = st.session_state.get("staff_id")
staff_name = st.session_state.get("staff_name")
company_name = st.session_state.get("company_name")
organizational_unit = st.session_state.get("organizational_unit")
attendance = st.session_state.get("attendance")
timestamp = st.session_state.get("timestamp")
checked_in = st.session_state.get("checked_in", False)

st.header("Pengesahan Kehadiran")

# Display staff info (disabled so cannot edit)
st.text_input("Staff ID", staff_id, disabled=True)
st.text_input("Nama", staff_name, disabled=True)
st.text_input("Company", company_name, disabled=True)
st.text_input("Unit", organizational_unit, disabled=True)
gap(1)

# Case 1: Already checked in (previously or session state)
if attendance == "Yes" or checked_in:
    st.success(
        f"✅ Anda telah check-in!\n\n"
        f"Nama: {staff_name if staff_name else '-'}  \n"
        f"Staff ID: {staff_id}  \n"
        f"Company: {company_name if company_name else '-'}  \n"
        f"Unit: {organizational_unit if organizational_unit else '-'}  \n"
        f"Masa Check-in: {timestamp}"
        f"\n\nSila laporkan diri di kaunter pendaftaran bersama **screenshot** laman web ini. Terima kasih."
    )

# Case 2: Not yet checked in → show button
else:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        checkin_clicked = st.button("CHECK-IN", use_container_width=True)

    if checkin_clicked:
        if not staff_id:
            st.error("❌ Staff ID tidak dijumpai.")
        else:
            conn = get_connection()
            cur = conn.cursor()

            # Save current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["timestamp"] = timestamp

            # Update attendance in DB
            cur.execute(
                "UPDATE union_member SET attendance = %s, checkin_time = %s WHERE staff_id = %s;",
                ("Yes", timestamp, staff_id)
            )
            conn.commit()

            cur.close()
            conn.close()

            # Mark as checked-in in session
            st.session_state["checked_in"] = True
            st.session_state["attendance"] = "Yes"

            # Show success info
            st.success(
                f"✅ Check-in berjaya!\n\n"
                f"Nama: {staff_name if staff_name else '-'}  \n"
                f"Staff ID: {staff_id}  \n"
                f"Company: {company_name if company_name else '-'}  \n"
                f"Unit: {organizational_unit if organizational_unit else '-'}  \n"
                f"Masa Check-in: {timestamp}"
                f"\n\nSila laporkan diri di kaunter pendaftaran bersama **screenshot** laman web ini. Terima kasih."
            )
