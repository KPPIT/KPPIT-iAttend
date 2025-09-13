import streamlit as st
import streamlit.components.v1 as components
import os

# --- Authentication Logic ---

def load_credentials():
    return st.secrets["users"]

def authenticate(username, password, credentials):
    return credentials.get(username) == password

# Create a component that can listen for messages
def create_message_listener():
    components.html("""
    <script>
        // Listen for messages from the login form
        window.addEventListener('message', function(event) {
            // Check if the message is from our login form
            if (event.data.type === 'login_request') {
                // Forward the message to Streamlit
                window.parent.postMessage({
                    type: 'streamlit_message',
                    data: event.data
                }, '*');
            }
        });
        
        // Notify that the message listener is ready
        console.log("Message listener ready");
    </script>
    """, height=0)

# --- Streamlit UI and Logic ---

def main():
    # Initialize session state with all required attributes
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.login_attempt = False
        # st.session_state.login_data = None

    # Add the message listener
    create_message_listener()
    
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            .main > div {
                padding-top: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Check if we have received login data via session state
    # if st.session_state.login_data and not st.session_state.logged_in:
    #     data = st.session_state.login_data
    #     st.session_state.login_attempt = True
        
    #     # Perform authentication
    #     credentials = load_credentials()
    #     if authenticate(data['username'], data['password'], credentials):
    #         st.session_state.logged_in = True
    #         st.session_state.username = data['username']
    #         # Clear the login data
    #         st.session_state.login_data = None
    #         st.rerun()
    #     else:
    #         # Clear the login data to allow for another attempt
    #         st.session_state.login_data = None
    #         st.rerun()

    # Listen for messages from the HTML component
    if not st.session_state.logged_in:
        # Create a container for the HTML component
        html_container = st.container()
        
        with html_container:
            # Read the HTML file
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                login_html_path = os.path.join(current_dir, "login.html")
                
                with open(login_html_path, "r", encoding="utf-8") as f:
                    html_code = f.read()
                
                # Create the HTML component
                components.html(html_code, height=450, key="login_form")
                
            except FileNotFoundError:
                st.error("Login form not found. Using fallback form.")
                # Fallback form in case HTML file is missing
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Login")
                    
                    if submitted:
                        credentials = load_credentials()
                        if authenticate(username, password, credentials):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error("Invalid username or password")

    # --- Display UI based on login state ---
    if st.session_state.logged_in:
        # This is the "dashboard" or main app content
        st.title(f"Welcome, {st.session_state.username}!")
        st.write("You are successfully logged in.")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.login_attempt = False
            st.session_state.login_data = None
            st.rerun()
    else:
        st.title("Login Required")
        
        # Debug info - can be removed after testing
        if st.session_state.get('login_attempt', False):
            st.warning("Login failed. Please check your credentials.")

# Listen for messages from the HTML component
components.html(
    """
    <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'login_request') {
                // Send the login data to Streamlit
                window.parent.postMessage({
                    type: 'streamlit_message',
                    data: event.data
                }, '*');
            }
        });
    </script>
    """,
    height=0
)

if __name__ == "__main__":
    main()