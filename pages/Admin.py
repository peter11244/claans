import pandas as pd
import streamlit as st

from src.models.claan import Claan
from src.models.dice import Dice
from src.models.task import TaskType
from src.utils import data
from src.utils.database import Database, initialise


def load_data():
    with Database.get_session() as session:
        st.session_state["tasks"] = data.get_tasks(_session=session)
        st.session_state["users"] = data.get_users(_session=session)
        for claan in Claan:
            st.session_state[f"users_{claan}"] = data.get_claan_users(
                _session=session, claan=claan
            )


def refresh_data():
    """Hard refresh of all data, including clearing data cache."""
    st.cache_data.clear()
    load_data()


def check_password():
    def password_entered():
        if st.session_state["admin_password"] == st.secrets["passwords"]["admin"]:
            st.session_state["admin_password_correct"] = True
            del st.session_state["admin_password"]
        else:
            st.session_state["admin_password_correct"] = False

    if st.session_state.get("admin_password_correct", False) or st.secrets.get(
        "env"
    ).get("debug", False):
        return True

    st.text_input(
        "Admin Password",
        type="password",
        on_change=password_entered,
        key="admin_password",
    )

    if "password_correct" in st.session_state:
        st.error("Incorrect Admin Password.")

    return False


@st.experimental_fragment
def delete_user_form():
    with st.container(border=True):
        st.subheader("Delete User")
        claan = st.selectbox(
            label="Claan",
            key="delete_user_claan",
            options=Claan,
            format_func=lambda claan: claan.value,
        )
        user = None
        if claan:
            user = st.selectbox(
                label="User",
                key="delete_user_selection",
                options=st.session_state[
                    f"users_{st.session_state["delete_user_claan"]}"
                ],
                format_func=lambda user: user.name,
            )

        submit_enabled = claan and user
        if st.button(
            "Submit",
            type="primary",
            disabled=not submit_enabled,
            on_click=data.delete_user,
            kwargs={"_session": Database.get_session()},
        ):
            st.rerun()


def user_management() -> None:
    with st.container(border=True):
        st.subheader("User Management")

        col_df, col_forms = st.columns(2)

        with col_df:
            df_users = pd.DataFrame.from_records(
                data=[vars(user) for user in st.session_state["users"]]
            )
            if "_sa_instance_state" in df_users.columns:
                df_users.drop("_sa_instance_state", inplace=True, axis=1)
            if "claan" in df_users.columns:
                df_users["claan"] = df_users["claan"].apply(lambda x: x.value)

            st.dataframe(
                data=df_users,
                use_container_width=True,
                hide_index=True,
                column_config={"name": "Name", "claan": "Claan"},
            )
        with col_forms:
            with st.form(key="add_user", clear_on_submit=True, border=True):
                st.subheader("Add User")
                st.text_input(label="Name", key="add_user_name", placeholder="John Doe")
                st.text_input(label="Email", key="add_user_email", placeholder="John.Doe@advancinganalytics.co.uk")
                st.selectbox(
                    label="Claan",
                    key="add_user_claan",
                    options=Claan,
                    format_func=lambda claan: claan.value,
                )
                st.form_submit_button(
                    label="Submit",
                    on_click=data.add_user,
                    kwargs={"_session": Database.get_session()},
                )
            delete_user_form()


@st.experimental_fragment
def set_active_quest_form():
    with st.container(border=True):
        st.subheader("Set Active Quest")
        quest_dice = st.selectbox(
            label="Dice to Update",
            key="set_active_quest_dice",
            options=list(Dice),
            format_func=lambda dice: dice.name,
        )
        quest_selection = None
        if quest_dice:
            quest_selection = st.selectbox(
                label="Quest",
                key="set_active_quest_selection",
                options=[
                    task
                    for task in st.session_state["tasks"]
                    if task.dice == quest_dice and task.task_type == TaskType.QUEST
                ],
                format_func=lambda task: task.description,
            )
        if st.button(
            label="Submit",
            key="set_active_quest_submit",
            disabled=not (quest_dice and quest_selection),
            on_click=data.set_active_task,
            kwargs={"_session": Database.get_session(), "task_type": TaskType.QUEST},
        ):
            st.rerun()


@st.experimental_fragment
def set_active_activity_form():
    with st.container(border=True):
        st.subheader("Set Active Activity")
        activity_dice = st.selectbox(
            label="Dice to Update",
            key="set_active_activity_dice",
            options=[Dice.D4, Dice.D6, Dice.D8, Dice.D10],
            format_func=lambda dice: dice.name,
        )
        activity_selection = None
        if activity_dice:
            activity_selection = st.selectbox(
                label="Activity",
                key="set_active_activity_selection",
                options=[
                    task
                    for task in st.session_state["tasks"]
                    if task.dice == activity_dice
                    and task.task_type == TaskType.ACTIVITY
                ],
                format_func=lambda task: task.description,
            )
        if st.button(
            label="Submit",
            key="set_active_activity_submit",
            disabled=not (activity_dice and activity_selection),
            on_click=data.set_active_task,
            kwargs={
                "_session": Database.get_session(),
                "task_type": TaskType.ACTIVITY,
            },
        ):
            st.rerun()


def task_management() -> None:
    with st.container(border=True):
        st.subheader("Task Management")

        col_df, col_forms = st.columns(2)

        with col_df:
            df_tasks = pd.DataFrame.from_records(
                data=[vars(task) for task in st.session_state["tasks"]]
            )
            if "_sa_instance_state" in df_tasks.columns:
                df_tasks.drop("_sa_instance_state", inplace=True, axis=1)
            if "dice" in df_tasks.columns:
                df_tasks["dice"] = df_tasks["dice"].apply(lambda x: x.value)
            if "task_type" in df_tasks.columns:
                df_tasks["task_type"] = df_tasks["task_type"].apply(lambda x: x.value)
            st.dataframe(
                data=df_tasks,
                use_container_width=True,
                hide_index=True,
            )
        with col_forms:
            set_active_quest_form()
            set_active_activity_form()
            with st.form(key="add_task", clear_on_submit=True, border=True):
                st.subheader("Add Task")
                st.text_input(label="Description", key="add_task_description")
                st.selectbox(
                    label="Type",
                    key="add_task_type",
                    options=TaskType,
                    format_func=lambda type: type.name.capitalize(),
                )
                st.selectbox(
                    label="Dice",
                    key="add_task_dice",
                    options=Dice,
                    format_func=lambda die: die.name,
                )
                st.toggle(
                    label="Ephemeral",
                    key="add_task_ephemeral",
                    help="When true, task may only be active once",
                )
                st.form_submit_button(
                    label="Submit",
                    on_click=data.add_task,
                    kwargs={"_session": Database.get_session()},
                )
            with st.form(key="delete_task", clear_on_submit=True, border=True):
                st.subheader("Delete Task")
                st.selectbox(
                    label="Task",
                    key="delete_task_selection",
                    options=list(st.session_state["tasks"]),
                    format_func=lambda task: task.description,
                )
                st.form_submit_button(
                    label="Submit",
                    on_click=data.delete_task,
                    kwargs={"_session": Database.get_session()},
                )


def init_page() -> None:
    st.set_page_config(page_title="Admin", layout="wide")

    if not check_password():
        st.stop()

    load_data()

    with st.container(border=True):
        st.header("Admin Page")

        st.button(
            label="Initialise Database",
            key="button_init_data",
            on_click=initialise,
        )
        st.button(
            label="Refresh Data", key="button_refresh_data", on_click=refresh_data
        )

        user_management()
        task_management()


if __name__ == "__main__":
    init_page()
