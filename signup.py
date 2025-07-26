import streamlit as st
from firebase_config import auth

def signup_form():
    st.subheader("Create New Account")
    first_name = st.text_input("First Name", key="reg_first")
    last_name = st.text_input("Last Name", key="reg_last")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        if not email or not password:
            st.error("Email and Password are required.")
        else:
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Registration successful! Please log in.")
            except Exception as e:
                error_message = str(e)
                if "EMAIL_EXISTS" in error_message:
                    st.error("Email already registered.")
                else:
                    st.error("Registration failed. Try again.")