import streamlit as st
from pathlib import Path

# Function to create spacing
def spacing_placeholder(lines: int = 1):
    for _ in range(lines):
        st.write("")

# Function to load images from the /images folder

# cache_data : suitable for data processing, API calls, loading CSVs/DataFrames
@st.cache_data(ttl=43200) # cache for 12 hour
def load_image(filename: str):  
        current_dir = Path(__file__).parent   # points to /iAttend
        # image_path = current_dir / "images" / filename
        # return st.image(image_path)
        return current_dir / "images" / filename

# Function to load and inject CSS
@st.cache_data(ttl=43200)
def load_css(file_name):
    """Loads and injects a CSS file ."""
    with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to load and display Markdown
@st.cache_data(ttl=43200)
def load_markdown(file_name):
    """Loads and displays a markdown notes file."""
    with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f.read(), unsafe_allow_html=True)
