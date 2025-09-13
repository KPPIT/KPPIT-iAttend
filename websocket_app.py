import streamlit as st
from live_component import my_live_data_component

st.title("📡 Live WebSocket Data")
data = my_live_data_component("ws://localhost:1000/ws", key="live")

st.write("Raw data received:")
st.json(data)
