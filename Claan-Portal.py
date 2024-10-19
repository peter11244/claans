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
    st.write("Welcome to Claans! Please sign in to continue.")
    st.stop()

else:
    # name = auth_data["account"]["name"]
    email = auth_data["account"]["username"]
    with Database.get_session() as session:
        if "current_user" not in st.session_state:
            st.session_state["current_user"] = get_current_user(session, email)
    st.switch_page("pages/0_Home.py")
    





menu() # Render the dynamic menu!