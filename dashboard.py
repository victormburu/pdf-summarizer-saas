import streamlit as st
from summarizer import summarize_text
from utils.pdf_handler import extract_text_from_pdf
from subscription import subscription_page
from utils.auth_utils import is_user_paid

def show_dashboard():
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("PLease log in first.")
        return

    user_email = st.session.state.user["email"]
    if not is_user_paid(user_email):
        st.warning("You must subcribe before acessinf the PDF Summarizer")
        st.session_state.page = "SUbscription"
        st.stop()

        # Now only paid users can proceed
    st.markdown("Upload your PDF below")

    st.success("Access granted to PDF Summarizer")
    dashboard()


def dashboard():
    st.title("📄 SmartDoc PDF Summarizer")
    st.info("Upload your PDF file to summarize")
    st.markdown("Upload your PDF below")
    uploaded_file = st.file_uploader("Upload your PDF", type=["PDF"])

    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        #st.experimental_rerun()

    if uploaded_file:
        with st.spinner("Extracting text ..."):
            raw_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Original Text (First 1000 chars)")
        st.write(raw_text[:1000])

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(raw_text[:3000])
                st.subheader("Summary")
                st.write(summary)


subscription_page()