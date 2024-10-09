import pathlib

import streamlit as st
from streamlit_msal import Msal

from src.models.claan import Claan
from src.utils import data
from src.utils.database import Database


def init_page() -> None:
    st.set_page_config(page_title="Claan ChAAos", page_icon=":dragon:")
    
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

    available_pages = [st.Page("./pages/Home.py")]
    if auth_data:


         # Getting useful information
        access_token = auth_data["accessToken"]

        account = auth_data["account"]
        name = account["name"]
        username = account["username"]
        account_id = account["localAccountId"]

        # IF CLAAN
        available_pages.append(st.Page("./pages/Thunder_Walkers.py"))
        # IF ADMIN
        available_pages.append(st.Page("./pages/Admin.py"))

        pg = st.navigation(
            pages=available_pages,
            position="sidebar",
        )
        pg.run()

    else:
        pg = st.navigation(pages=available_pages, position="hidden")
        pg.run()
        st.write("Welcome to CLAANS! Please Log In.")
        st.stop()

def main() -> None:
    init_page()


if __name__ == "__main__":
    main()
