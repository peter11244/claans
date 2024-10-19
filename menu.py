import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/0_Home.py", label="Claans Home")
    # Clean Up
    match st.session_state["current_user"].claan.value:
        case "Earth Striders":
            st.sidebar.page_link("pages/1_Earth_Striders.py", label="Earth Striders")
        case "Fire Dancers":
            st.sidebar.page_link("pages/2_Fire_Dancers.py", label="Fire Dancers")
        case "Thunder Walkers":
            st.sidebar.page_link("pages/3_Thunder_Walkers.py", label="Thunder Walkers")
        case "Wave Riders":
            st.sidebar.page_link("pages/4_Wave_Riders.py", label="Wave Riders")
        case "Beast Runners":
            st.sidebar.page_link("pages/5_Beast_Runners.py", label="Beast Runners")
        case "Iron Stalkers":
            st.sidebar.page_link("pages/6_Iron_Stalkers.py", label="Iron Stalkers")
    # Add admin flag for users
    if st.session_state["current_user"].email == "peter.sach@advancinganalytics.co.uk":
        st.sidebar.page_link("pages/7_Admin.py", label="Manage users")
    st.sidebar.page_link("pages/Claan-Portal-Logout.py", label="Log Out")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Claan-Portal.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "current_user" not in st.session_state:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "current_user" not in st.session_state:
        st.switch_page("Claan-Portal.py")
    menu()