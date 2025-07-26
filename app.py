import streamlit as st
from login import login_form
from signup import signup_form
from dashboard import dashboard
from subscription import show_subscription

st.set_page_config(page_title="SmartDoc AI")

# --- SESSION SETUP ---
if "user" not in st.session_state:
    st.session_state.user = None
if "paid" not in st.session_state:
    st.session_state.paid = False
if "page" not in st.session_state:
    st.session_state.page = "Login/Register"

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔐 SmartDoc AI")
page = st.sidebar.selectbox(
    "📚 Navigation",
    ["Login/Register", "Summarize PDF"],
    index=["Login/Register", "Summarize PDF"].index(st.session_state.page)
)

# --- LOGIN / SIGNUP PAGE ---
if page == "Login/Register":
    auth_mode = st.radio("Choose Mode", ["Login", "Register"])
    if auth_mode == "Login":
        login_form()
    else:
        signup_form()

# --- PDF DASHBOARD PAGE ---
elif page == "Summarize PDF":
    if not st.session_state.user:
        st.warning("🔐 Please log in first.")
    else:
        if not st.session_state.paid:
            st.warning("💳 Please complete payment to access the PDF summarizer.")
            show_subscription()
        else:
            dashboard()
