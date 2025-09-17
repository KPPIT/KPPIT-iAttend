import streamlit as st 
from utils import load_image
from db import get_by_query
from pengesahan import confirmation

st.set_page_config(page_title="iAttend", page_icon="🌐", layout="centered", initial_sidebar_state="collapsed")

# --- All Custom CSS in one block ---
st.markdown("""
<style>
/* Centering the image and reducing spacing */
.stImage {
    width: 50%;
    display: flex;
    justify-content: center;
    margin-bottom: -35px;   /* Reduce space below image */
    margin-top: -50px;      /* Reduce space above image */
}
.stTextInput input[type="text"] {
        background-color: #e2dadbff;
        padding: 2px;
        color: #043464;
        caret-color: #043464;
}
/* Style for the notes list */
.notes-list {
    padding: 5px;
    margin-top: -15px;      /* Reduce space above notes */
    margin-bottom: -15px;   /* Reduce space below notes */
}
/* Style for the button */
.stButton>button {
    background-color: #4d6d8dff;
    color: #fff;
    padding: 5px;
    border-radius: 8px;
    cursor: pointer;
}
.stButton>button:hover {
    background-color: #71aae4;
}
</style>
""", unsafe_allow_html=True)

# Banner image
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    st.image(load_image('KPPIT.png'))

# Page header  
st.header("Mesyuarat Agung KPPIT Kali ke-31")

# render the widgets
input_staff_id = st.text_input("Sila masukkan Staff ID anda : ")

# Nota penting
st.markdown("""
<div class="notes-list">
<b>Nota penting:</b>
<ul  style="font-size: 13px; padding-left: 20px; margin-bottom: -5px;">
    <li>Anda wajib merekodkan kehadiran anda menggunakan aplikasi ini</li>
    <li>Majlis ini hanya terbuka kepada ahli KPPIT (Ogos) sahaja</li>
    <li>Pastikan Staff ID yang dimasukkan adalah sama seperti yang tertera pada batch pekerja anda</li>
    <li>Contoh: <i>05XXXXXX / 30XXXXXX</i> </li>
</ul>
</div>
<style>
    .stToast {
        background-color: #e2dadbff;
        color:#043464;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

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
            query = "SELECT staff_id, employee_name, company_name, organizational_unit, attendance, checkin_time FROM union_member WHERE staff_id = %s"
            staff, _ = get_by_query(query=query, params=(clean_staff_id,), single_row=True)

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
