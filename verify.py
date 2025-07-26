import re
import streamlit as st

st.title("🔐 Login Page")

email = st.text_input("email", key="login_email")

if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    st.warning("⚠️ Please enter a valid email address.")
else:
    st.success("✅ Email format is valid. Proceeding with login...")