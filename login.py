import streamlit as st
import requests
from firebase_config import auth
from utils.logger import log_disabled_user


def login_form():
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email.strip().lower(), password)
            st.session_state.user = user
            st.success(f"Welcome back, {st.session_state.user['email']}!")
            st.session_state.page = "Summarize PDF"

        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json()["error"]["message"]
                if error == "USER_DISABLED":
                    log_disabled_user(email)
                    st.warning("🚫 Your account has been disabled. Contact support.")
                elif error == "EMAIL_NOT_FOUND":
                    st.error("❌ Email not registered.")
                elif error == "INVALID_PASSWORD":
                    st.error("❌ Incorrect password.")
                else:
                    st.error(f"Login failed: {error}")
            except:
                st.error(f"Unexpected error: {e}")

    st.markdown("---")
    st.subheader("🔁 Forgot Password?")
    reset_email = st.text_input("Enter your email to reset password", key="reset_email")
    if st.button("Send Reset Email"):
        try:
            auth.send_password_reset_email(reset_email.strip().lower())
            st.success("✅ Password reset email sent.Please check your inbox")

        except Exception as e:
            try:
                error = e.response.json()["error"]["message"]
                if error == "EMAIL_NOT_FOUND":
                    st.error("❌ Email not registered.")
                elif error == "INVALID_EMAIL":
                    st.error("❌ Invalid email format.")
                else:
                    st.error("❌ Could not send reset email.")
            except:
                st.error("⚠️ Unexpected error occurred during password reset.")

# Payment section
