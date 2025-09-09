import streamlit as st 
from PIL import Image 
from utils import load_image, spacing_placeholder
from db import check_staff   # <-- use your db.py connection
from pengesahan import confirmation
from styling import set_page_style

# --- UI Setup ---
st.set_page_config(page_title="iAttend", page_icon="🌐", layout="centered", initial_sidebar_state="collapsed")
set_page_style()

# --- Main Page Content ---
img = load_image("kppit.png")
if img:
    st.image(img, width='stretch')
            #width='content' behaves like the old use_container_width=False
            #width='stretch' behaves like the use_container_width=True

spacing_placeholder(1)

st.header("Majlis KPPIT")

input_staff_id = st.text_input("Sila masukkan staff ID anda untuk membuat pengesahan: ")

st.caption("""Nota penting:  
- Majlis ini hanya terbuka kepada ahli berdaftar sahaja  
- Pastikan staff ID yang dimasukkan adalah betul dan lengkap  
- Staff ID hanya mengandungi nombor sahaja  
- Contoh: 12345678""")

col1, col2, col3 = st.columns([3, 2, 3])  
with col2:
    if st.button("CHECK STAFF ID", width='stretch'): 
            #width='content' behaves like the old use_container_width=False
            #width='stretch' behaves like the old use_container_width=True

        # If empty input
        if input_staff_id.strip() == "":
            st.toast("Sila masukkan staff ID anda.")

        # If contains non-digit characters
        elif not input_staff_id.isdigit():  
            st.toast("Staff ID hanya boleh mengandungi nombor.")

        else:
            # --- Check DB for staff ---
            staff = check_staff(input_staff_id)

            if staff:
                st.session_state["staff_id"] = staff[0]
                st.session_state["staff_name"] = staff[1]
                st.session_state["company_name"] = staff[2]
                st.session_state["organizational_unit"] = staff[3]
                st.session_state["attendance"] = staff[4]
                st.session_state["timestamp"] = staff[5].strftime("%Y-%m-%d %H:%M:%S") if staff[5] else None

                # Open small dialog to check in / check done check in
                confirmation()

            else:
                st.toast("Maaf, nama anda tidak tersenarai sebagai ahli berdaftar.", )