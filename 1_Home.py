import streamlit as st 
from utils import load_image, load_css, load_markdown
from db import get_by_query
from pengesahan import confirmation

st.set_page_config(page_title="iAttend", page_icon="🌐", layout="centered", initial_sidebar_state="collapsed")

# Call the function to load the CSS file
load_css("style.css")

# Banner image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(load_image('KPPIT.webp'), width="stretch")

# Page header  
st.header("Mesyuarat Agung KPPIT Kali ke-31")

# render the widgets
input_staff_id = st.text_input("Sila masukkan Staff ID anda : ")

# Call the function to load the Markdown notes
load_markdown("notes.md")

# Center the button using columns
col1, col2, col3 = st.columns([3, 2, 3])  
with col2:
    if st.button("CEK ID", width='stretch'): 

       # Remove spaces 
        clean_staff_id = "".join(input_staff_id.split())

        # If empty input
        if not clean_staff_id:
            st.toast("Sila masukkan staff ID anda.")

        # If contains non-digit characters
        elif not clean_staff_id.isdigit():  
            st.toast("Staff ID hanya boleh mengandungi nombor.")

        else:
            # --- Check DB for staff ---
            query = "SELECT staff_id, name, attendance, checkin_time FROM union_members WHERE staff_id = %s"
            staff, _ = get_by_query(query=query, params=(clean_staff_id,), single_row=True)

            if staff:
                st.session_state["staff_id"] = staff[0]
                st.session_state["name"] = staff[1]
                st.session_state["attendance"] = staff[2]
                st.session_state["timestamp"] = staff[3].strftime("%Y-%m-%d %H:%M:%S") if staff[3] else None

                # Open small dialog to check in / check done check in
                confirmation()

            else:
                st.toast("Maaf, nama anda tidak tersenarai sebagai ahli berdaftar.", )
