import streamlit as st
from pathlib import Path
from PIL import Image

# Function to create spacing
def spacing_placeholder(lines: int = 1):
    for _ in range(lines):
        st.write("")

# Function to load images from the /images folder
def load_image(filename: str):  
        
        current_dir = Path(__file__).parent   # points to /iAttend
        image_path = current_dir / "images" / filename
        return Image.open(image_path)
