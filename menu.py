import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/0_Home.py", label="Claans Home")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/7_Admin.py", label="Manage users")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Claan-Portal.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "current_user" not in st.session_state:
        st.switch_page("Claan-Portal.py")
    menu()