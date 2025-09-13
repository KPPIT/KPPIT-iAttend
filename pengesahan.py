import streamlit as st
from datetime import datetime, timedelta
from utils import spacing_placeholder
from db import get_connection

def show_success_msg(success_msg, staff_id, staff_name, company_name, organizational_unit, timestamp):
    st.success(
    f"{success_msg}\n\n"
    f"**Nama:**\n\n{staff_name if staff_name else '-'}\n\n"
    f"**Staff ID:**\n\n{staff_id}\n\n"
    f"**Department:**\n\n{organizational_unit if organizational_unit else '-'}\n\n"
    f"**Masa Check-in:**\n\n{timestamp}\n\n"
    f"Sila lapor diri di kaunter pendaftaran bersama **ID + SNAPSHOT** page ini untuk mengambil **kupon makanan dan cabutan bertuah**. Terima kasih."
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

    # Case 1: Already checked in (previously or session state)
    if attendance == "Yes":
        # Display success message
        show_success_msg("✅ ANDA TELAH CHECK-IN !", staff_id, staff_name, company_name, organizational_unit, timestamp)

    # Case 2: Not yet checked in → show button
    else:

        #Put the form inside a placeholder so we can hide it later
        form_area = st.empty() 

        with form_area.container(): 
            
            # Custom CSS to make rectangular boxes
            st.markdown("""
                <style>
                .info-box {
                    background-color: #f0f2f6;   /* light grey background */
                    border: 1px solid #ccc;      /* border like text_input */
                    padding: 8px 12px;           /* inner spacing */
                    border-radius: 10px;          /* rounded corners */
                    margin-bottom: 2px;         /* spacing between boxes */
                    font-weight: bold;           /* make text bold */
                    color: #000000;              /* black font for contrast */
                }
                </style>
            """, unsafe_allow_html=True)

            # Now render each info in a styled box
            st.subheader("Staff ID")
            st.markdown(f"<div class='info-box'>{staff_id}</div>", unsafe_allow_html=True)

            st.subheader("Nama")
            st.markdown(f"<div class='info-box'>{staff_name}</div>", unsafe_allow_html=True)

            st.subheader("Company")
            st.markdown(f"<div class='info-box'>{company_name}</div>", unsafe_allow_html=True)

            st.subheader("Department")
            st.markdown(f"<div class='info-box'>{organizational_unit}</div>", unsafe_allow_html=True)

            spacing_placeholder(1)


            col1, col2, col3 = st.columns([2, 3, 2])
            with col2:
                checkin_clicked = st.button("CHECK-IN", width='stretch')

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
                    "UPDATE union_member SET attendance = %s, checkin_time = %s WHERE staff_id = %s;",
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
                show_success_msg("✅ CHECK-IN BERJAYA !", staff_id, staff_name, company_name, organizational_unit, timestamp)  