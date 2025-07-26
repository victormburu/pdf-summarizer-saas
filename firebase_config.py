import pyrebase
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

firebaseconfig = {
    "apiKey": ("AIzaSyCLWkdQZHNf4c-a7jTj8vT1fhdiyGcFudo"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "projectId": os.getenv("projectID"),
    "storageBucket": os.getenv("storageBucket"),
    "messageSenderId": os.getenv("messageSenderID"),
    "appId": os.getenv("appID"),
    "measurementId": os.getenv("measurementID")
}

# DEBUG: Print one env value to confirm loading
#rint("✅ apiKey from ENV:", os.getenv("apiKey"))

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()

email = st.text_input("Email", key="login_email")
password = st.text_input("Password", type="password", key="login_password")

if st.button("Login"):
    if not email or not password:
        st.warning("Please enter both email and password.")
    else:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login successful!")
        except Exception as e:
            error_json = e.args[1]
            if "INVALID_LOGIN_CREDENTIALS" in error_json:
                st.error("Invalid email or password. Try again.")
            else:
                st.error(f"Unexpected error: {error_json}")


