import streamlit as st
from menu import menu
from streamlit_msal import Msal
from src.utils.data.users import get_current_user
from src.utils.database import Database

auth_data = Msal.initialize_ui(
        client_id="866dd59e-3ab4-41af-91fe-510d7ad9113e",
        authority="https://login.microsoftonline.com/6d2c78dd-1f85-4ccb-9ae3-cd5ea1cca361",
        scopes=[], # Optional
        # Customize (Default values):
        connecting_label="Connecting",
        disconnected_label="Disconnected",
        sign_in_label="Sign in",
        sign_out_label="Sign out"
    )

if not auth_data:
    st.session_state.pop("current_user")
    st.switch_page("Claan-Portal.py")

menu() # Render the dynamic menu!

