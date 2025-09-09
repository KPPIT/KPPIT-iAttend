#UI styling and layout
import streamlit as st

def set_page_style():
    """
    Applies custo#m CSS styling for the Streamlit application.
    """
    st.markdown("""
    <style>
        /* Styling for st.header */
    h2 {
        color: #FFFFFF; /*White*/
        font-size: 35px;
        font-family: 'Georgia', serif;
        font-weight: bold;
        padding: 10px;
        text-align: center;
    }
        /* Styling for the st.text_input label and input box */
        .stTextInput label {
            color: #FA0505; /*Red*/
            font-weight: bold;
        }
        .stTextInput div[data-testid="stTextInput"] > div > input {
            border: 5px solid #000000;
            border-radius: 8px;
            background-color: #F0FFF0; /* Honeydew */
        }

        /* Styling for st.caption */
        div[data-testid="stCaptionContainer"] p {
            font-size: 15px;
            color: #FFFFFF; 
            line-height: 1.5;
        }
        /* CSS to disable vertical scrolling */
        [data-testid="stAppViewContainer"] {
             overflow-y: hidden !important;
	}

    </style>
    """, unsafe_allow_html=True)