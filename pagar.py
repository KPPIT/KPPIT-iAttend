import streamlit as st
import time

# Load user credentials from secrets
def load_credentials():
    return st.secrets["users"]

# Check if the provided credentials are correct
def authenticate(username, password, credentials):
    return credentials.get(username) == password

def main():

    st.markdown("""
    <style>
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
        .stTextInput input[type="text"] {
            background-color: #e2dadbff;
            padding: 8px;
            color: #043464;
            caret-color: #043464;
            }
        .stToast {
            background-color: #e2dadbff;
            color:#043464;
            padding: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.show_success = False

    # Load credentials
    credentials = load_credentials()

    if not st.session_state.logged_in:
        st.title("Login")
        # Create login form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password, credentials):
                st.session_state.logged_in = True
                st.session_state.show_success = True
                st.toast("Login successful!")
                time.sleep(1)
                st.rerun()
                
            else:
                st.toast("Invalid username or password")
