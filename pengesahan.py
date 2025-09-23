import streamlit as st
from datetime import datetime, timedelta
from utils import spacing_placeholder, load_css
from db import get_connection

@st.cache_resource
def show_success_msg(success_msg, staff_id, staff_name, timestamp):
    st.success(
    f"{success_msg}\n\n"
    f"**Nama:**\n\n{staff_name if staff_name else '-'}\n\n"
    f"**Staff ID:**\n\n{staff_id}\n\n"
    f"**Masa:**\n\n{timestamp}\n\n"
    f"Sila lapor diri di kaunter pendaftaran bersama **ID + SNAPSHOT** page ini untuk mengambil **kupon makanan dan cabutan bertuah**. Terima kasih."
)

# add streamlit dialog
@st.dialog("Pengesahan Kehadiran")

def confirmation():

    # Retrieve data from session_state
    staff_id = st.session_state.get("staff_id")
    staff_name = st.session_state.get("name")
    attendance = st.session_state.get("attendance")
    timestamp = st.session_state.get("timestamp")

    # Case 1: Already checked in (previously or session state)
    if attendance == "Yes":
        # Display success message
        show_success_msg("✅ ANDA TELAH DAFTAR !", staff_id, staff_name, timestamp)

    # Case 2: Not yet checked in → show button
    else:

        #Put the form inside a placeholder so we can hide it later
        form_area = st.empty() 

        with form_area.container(): 
            
            # Call the function to load the CSS file
            load_css("style.css")

            # Now render each info in a styled box
            st.subheader("Staff ID")
            st.markdown(f"<div class='info-box'>{staff_id}</div>", unsafe_allow_html=True)

            st.subheader("Nama")
            st.markdown(f"<div class='info-box'>{staff_name}</div>", unsafe_allow_html=True)

            spacing_placeholder(1)

            col1, col2, col3 = st.columns([2, 3, 2])
            with col2:
                checkin_clicked = st.button("Daftar", width='stretch')

        if checkin_clicked:
            if not staff_id:
                st.error("❌ Staff ID tidak dijumpai.")
            else:
                # Connect to database connection pool
                db_pool = get_connection()
                conn = db_pool.getconn()
                cur = conn.cursor()

                # Save current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Note: timestamp in GMT on Render

                # Change timestamp to MYT (UTC +8:00)
                timestamp_to_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                timestamp_to_str_MYT = timestamp_to_str + timedelta(hours=8)
                timestamp = timestamp_to_str_MYT.strftime("%Y-%m-%d %H:%M:%S")  # timestamp in MYT

                # Update attendance in DB
                cur.execute(
                    "UPDATE union_members SET attendance = %s, checkin_time = %s WHERE staff_id = %s;",
                    ("Yes", timestamp, staff_id)
                )
                conn.commit()
                print("Data added successfully")

                if cur: 
                    cur.close()
                if conn:
                    db_pool.putconn(conn)
                    print("Database connection pool: Disconnected")

                # Mark as checked-in in session
                st.session_state["attendance"] = "Yes"
                st.session_state["timestamp"] = timestamp   

                # Hide the form and show only the success message 
                form_area.empty()  
                show_success_msg("✅ PENDAFTARAN BERJAYA !", staff_id, staff_name, timestamp)  