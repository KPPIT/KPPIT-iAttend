import streamlit as st
import streamlit.components.v1 as components

with open("login.html", "r") as f:
    html_code = f.read()

# Apply custom CSS to center the main container on the page.
st.markdown(
    """
    <style>
        .st-emotion-cache-18ni2cb, .st-emotion-cache-4u312j {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    components.html(html_code, height=600)