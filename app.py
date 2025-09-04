import streamlit as st 
from PIL import Image 
from utils import load_image, gap
from db import get_connection   # <-- use your db.py connection

st.set_page_config(page_title="iAttend", page_icon="🌐", layout="centered")

# --- Function to validate staff ID ---
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

# --- UI ---
img = load_image("kppit.png")
if img:
    st.image(img, use_container_width=True)

gap(2)
st.header("Majlis Mesyuarat Agung KPPIT 2025")
gap(2)

x = st.text_input("Sila masukkan staff ID anda untuk membuat pengesahan: ")
st.caption("Nota penting: \n - Majlis ini hanya terbuka kepada ahli berdaftar sahaja \n "
"- Pastikan staff ID yang dimasukkan adalah betul dan lengkap\n "
"- Staff ID hanya mengandungi nombor sahaja \n - Contoh: 12345678")

gap(1)

col1, col2, col3 = st.columns([3, 2, 3])  
with col2:
    if st.button("CEK", use_container_width=True):

        # If empty input
        if x.strip() == "":
            st.session_state["error_msg"] = "Sila masukkan staff ID anda."

        # If contains non-digit characters
        elif not x.isdigit():  
            st.session_state["error_msg"] = "Staff ID hanya boleh mengandungi nombor."

        else:
            # --- Check DB for staff ---
            staff = check_staff(x)

            if staff:
                st.session_state["staff_id"] = staff[0]
                st.session_state["staff_name"] = staff[1]
                st.session_state["company_name"] = staff[2]
                st.session_state["organizational_unit"] = staff[3]
                st.session_state["attendance"] = staff[4]
                st.session_state["timestamp"] = staff[5].strftime("%Y-%m-%d %H:%M:%S") if staff[5] else None

                # If valid staff → go pengesahan
                st.switch_page("pages/2_pengesahan.py")

            else:
                st.session_state["error_msg"] = "Maaf, nama anda tidak tersenarai sebagai ahli berdaftar."

# --- Show error inline ---
if "error_msg" in st.session_state:
    st.error(st.session_state["error_msg"])

