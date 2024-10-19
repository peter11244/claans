import pathlib

import streamlit as st

from src.models.claan import Claan
from src.utils.data.users import get_current_user
from src.utils.data.scores import get_scores
from src.utils.data.stocks import get_corporate_data
from src.utils.database import Database
from src.utils.logger import LOGGER

from streamlit_msal import Msal


def login() -> None:
    

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
        st.write("Welcome to Claans! Please sign in to continue.")
        st.stop()

    else:
        # name = auth_data["account"]["name"]
        email = auth_data["account"]["username"]
        with Database.get_session() as session:
            if "current_user" not in st.session_state:
                # TODO: Ensure single user?
                st.session_state["current_user"] = get_current_user(session, email)[0]


st.set_page_config(page_title="Claans Corporate Claash", page_icon=":dragon:")


###
## USER AUTH
###

# TODO: This approach can lead to the sign out button disappearing...
# Would like a way to skip the sign in box if possible for a repeated session
if "current_user" not in st.session_state:
    login() 

st.write(f"Hello {st.session_state["current_user"].name}!")
st.write(f"Your Email: {st.session_state["current_user"].email}")
st.write(f"Your Claan: {st.session_state["current_user"].claan.value}")


###
##  FILTERED NAV
###

available_pages = [st.Page("Claan-Portal.py")]

#Hacky
match st.session_state["current_user"].claan.value:
    case "Earth Striders":
        available_pages.append(st.Page("./pages/1_Earth_Striders.py"))
    case "Fire Dancers":
        available_pages.append(st.Page("./pages/2_Fire_Dancers.py"))
    case "Thunder Walkers":
        available_pages.append(st.Page("./pages/3_Thunder_Walkers.py"))
    case "Wave Riders":
        available_pages.append(st.Page("./pages/4_Wave_Riders.py"))
    case "Beast Runner":
        available_pages.append(st.Page("./pages/5_Beast_Runners.py"))
    case "Iron Stalkers":
        available_pages.append(st.Page("./pages/6_Iron_Stalkers.py"))

# TODO: Add an admin flag into the users table.
if st.session_state["current_user"].email == "peter.sach@advancinganalytics.co.uk":
    available_pages.append(st.Page("./pages/7_Admin.py"))

pg = st.navigation(pages=available_pages, position="sidebar")
pg.run()

