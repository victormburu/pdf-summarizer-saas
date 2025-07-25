from pickle import TRUE
import streamlit as st
from firebase_config import auth
from summarizer import summarize_text
from utils.pdf_handler import extract_text_from_pdf

st.set_page_config(page_title="AI PDF Summarizer")
st.title("AI Powered PDF Summarizer")

# --- SESSION STATE for user ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- SIDEBAR NAVIGATION ---
if "page" not in st.session_state:
    st.session_state.page = "Login/Register"
page = st.sidebar.selectbox("📚 Navigation", ["Login/Register", "Summarize PDF"],index=["Login/Register", "Summarize PDF"].index(st.session_state.page))

# --- LOGIN PAGE ---
if page == "Login/Register":
    st.title(" Login / Register")

    auth_mode = st.selectbox("choose mode", ["Login", "Register"])
# --- Login or Signup toggle ---

if auth_mode == "Register":
    st.subheader("Create New Account")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if not email or not password:
            st.error("Email and Password are required.")
        else:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success(f"Welcome, {first_name}! Please login now.")
                st.success("Registration successful! You can now log in.")

            except Exception as e:
                st.error(f"Registration error: {e}")
                if "EMAIL_EXISTS" in str(e):
                    st.error(" This email is already registered. Please log in instead.")
                else:
                    st.error(" Registration failed. Please try again.")
    
    if st.button("Forgot password?"):
        try:
            auth.send_password_reset_email(email)
            st.success("Password reset email sent. Check your inbox.")
        except Exception as e:
            st.error("Failed to send reset email.")

elif auth_mode == "Login":
    st.subheader("Login to your Account")
    email = st.text_input("Email").strip()
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email.strip().lower(), password)
            st.session_state.user = user["email"]
            st.success(f"Welcome back, {st.session_state.user}!")
            #st.experimental_rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")


#Only show file upload if user is logged in
if st.session_state.user:
    st.markdown("Upload your PDF below")
    uploaded_file = st.file_uploader("Upload your PDF", type=["PDF"])
    if uploaded_file is not None:
        with st.spinner("Extracting text ..."):
            raw_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Original Text (First 1000 chars)")
        st.write(raw_text[: 1000])

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(raw_text[:3000])
                st.subheader("summary")
                st.write(summary)
    else:
        st.warning("You must log in or register to upload and summarize PDF files.")

#payment methods
st.title("💳 Choose Your Payment Method")

payment_method = st.radio("Select Payment Method:", ["Paypal", "Mpesa", "Card"])

if payment_method == "Mpesa":
    st.markdown("[🇰🇪 Pay with Mpesa via Paystack](https://paystack.com/pay/mpesa-link)", unsafe_allow_HTML=TRUE)
elif payment_method == "Paypal":
    st.markdown("🌍 Pay with PayPal](https://www.paypal.com/paypalme/yourlink)", unsafe_allow_html=TRUE)
elif payment_method == "Card":
    st.markdown("[💳 Pay with Card (Flutterwave)](https://flutterwave.com/pay/yourproduct)", unsafe_allow_html=TRUE)
