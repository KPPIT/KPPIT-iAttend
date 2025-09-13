import os
import streamlit.components.v1 as components

_component_func = components.declare_component(
    "my_live_data_component",
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "build")
)

def my_live_data_component(websocket_url: str, key=None):
    return _component_func(websocketUrl=websocket_url, key=key)
