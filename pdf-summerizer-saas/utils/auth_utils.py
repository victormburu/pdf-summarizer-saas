import streamlit as st


def is_user_paid(user_email):
    paid_user = st.session_state.get("paid_user", [])
    return user_email in paid_user