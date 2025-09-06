import streamlit as st
from datetime import datetime, timedelta
from utils import spacing_placeholder
from db import get_connection

def show_success_msg(success_msg, staff_id, staff_name, company_name, organizational_unit, timestamp, checked_in=False):
    st.success(
            f"{success_msg}\n\n"
            f"Nama: {staff_name if staff_name else '-'}  \n"
            f"Staff ID: {staff_id}  \n"
            f"Company: {company_name if company_name else '-'}  \n"
            f"Unit of Department: {organizational_unit if organizational_unit else '-'}  \n"
            f"Masa Check-in: {timestamp}"
            f"\n\nPastikan anda **SNAPSHOOT** laman web ini."
            f"\n\nSila lapor diri di kaunter pendaftaran bersama **SNAPSHOOT** laman web ini. Terima kasih."
        )
# add streamlit dialog
@st.dialog("Pengesahan Kehadiran")

def confirmation():

    # Retrieve data from session_state
    staff_id = st.session_state.get("staff_id")
    staff_name = st.session_state.get("staff_name")
    company_name = st.session_state.get("company_name")
    organizational_unit = st.session_state.get("organizational_unit")
    attendance = st.session_state.get("attendance")
    timestamp = st.session_state.get("timestamp")
    checked_in = st.session_state.get("checked_in", False)

    # Case 1: Already checked in (previously or session state)
    if attendance == "Yes" or checked_in:
        # Display success message
        show_success_msg("✅ ANDA TELAH CHECK-IN !", staff_id, staff_name, company_name, organizational_unit, timestamp, checked_in=False)

    # Case 2: Not yet checked in → show button
    else:

        # Display staff info (disabled so cannot edit)
        st.text_input("Staff ID", staff_id, disabled=True)
        st.text_input("Nama", staff_name, disabled=True)
        st.text_input("Company", company_name, disabled=True)
        st.text_input("Unit", organizational_unit, disabled=True)
        spacing_placeholder(1)

        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            checkin_clicked = st.button("CHECK-IN", use_container_width=True)

        if checkin_clicked:
            if not staff_id:
                st.error("❌ Staff ID tidak dijumpai.")
            else:
                # Connect to db
                conn = get_connection()
                cur = conn.cursor()

                # Save current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Note: timestamp declare in GMT due to deploy in render

                # Change timestamp to MYT (UTC +8:00)
                timestamp_to_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                timestamp_to_str_MYT = timestamp_to_str + timedelta(hours=8)
                timestamp = timestamp_to_str_MYT.strftime("%Y-%m-%d %H:%M:%S") # timestamp declare in MYT

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

                show_success_msg("✅ CHECK-IN BERJAYA !", staff_id, staff_name, company_name, organizational_unit, timestamp, checked_in=False)
