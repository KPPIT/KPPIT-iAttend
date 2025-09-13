import streamlit as st 
from PIL import Image 
from utils import load_image, spacing_placeholder
from db import check_staff   # <-- use your db.py connection
from pengesahan import confirmation

st.set_page_config(page_title="iAttend", page_icon="🌐", layout="centered", initial_sidebar_state="collapsed")

# Banner image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
            st.image('KPPIT.png', width='stretch')
            #width='content' behaves like the old use_container_width=False
            #width='stretch' behaves like the use_container_width=True

# Page header  
st.header("Mesyuarat Agung KPPIT Kali ke-31")

# render the widgets
input_staff_id = st.text_input("Sila masukkan staff ID anda : ")

# Nota penting
st.markdown("""
<div class="notes-list">
<b>Nota penting:</b>
<ul>
    <li>Anda wajib merekodkan kehadiran anda menggunakan aplikasi ini</li>
    <li>Majlis ini hanya terbuka kepada ahli KPPIT (Ogos) sahaja</li>
    <li>Pastikan staff ID yang dimasukkan adalah sama seperti yang tertera pada batch pekerja anda</li>
    <li>Contoh: <i>05XXXXXX / 30XXXXXX</i> </li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stButton>button {
            background-color: #4d6d8dff;
            color: #fff;
            padding:10x;
            border-radius: 8px;
            border: #fff;
            cursor: pointer;
        }
    .stButton>button:hover {
            background-color: #71aae4;
            }
    </style>
""", unsafe_allow_html=True)

# Center the button using columns
col1, col2, col3 = st.columns([3, 2, 3])  
with col2:
    if st.button("CEK ID", width='stretch'): 
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
