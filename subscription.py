import streamlit as st
from utils.payment_utils import create_payment_link, check_payment_status

def show_subscription():
    st.header("💳 Subscribe to Unlock Summarizer")

    plan = st.selectbox("Choose Plan", ["Daily - KES 50", "Weekly - KES 200", "Monthly - KES 500"])
    
    if st.button("Pay Now"):
        email = st.session_state.get("user", {}).get("email", "guest@example.com")
        pay_link = create_payment_link(email, plan)
        st.markdown(f"[👉 Click here to pay]({pay_link})", unsafe_allow_html=True)
        st.info("✅ After payment, click the button below to verify access.")

    if st.button("🔄 Verify Payment"):
        email = st.session_state.get("user", {}).get("email", "guest@example.com")
        if check_payment_status(email):
            st.success("✅ Payment verified. You can now use the summarizer.")
            st.session_state.paid = True
        else:
            st.error("❌ Payment not found. Please try again.")

def subscription_page():
    st.title("Subscription Plans")
    st.write("Choose your access plan to use the SmartDoc AI summarizer.")
