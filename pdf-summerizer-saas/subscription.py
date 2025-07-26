import streamlit as st
from utils.payment_utils import create_payment_link, check_payment_by_reference, check_payment_status

def show_subscription():
    st.header("💳 Subscribe to Unlock Summarizer")

    plan = st.selectbox(
        "Choose Plan",
        ["Daily - KES 50", "Weekly - KES 200", "Monthly - KES 500"])

    payment_method = st.radio(
        "Choose Payment Method",
        ["Paystack (Africa)", "PayPal (Global)"]
        
    )
    
    if st.button("Pay Now"):
        email = st.session_state.get("user", {}).get("email", "guest@example.com")
        provider = "paystack" if "Paystack" in payment_method else "paypal"

        pay_link = create_payment_link(email, plan, provider)

        if pay_link:
            st.markdown(f"[👉 Click here to pay]({pay_link})", unsafe_allow_html=True)
            st.info("✅ After payment, click the button below to verify access.")
        else:
            st.error("❌ Failed to create payment. Try again.")

    if st.button("🔄 Verify Payment"):
        ref = st.session_state.get("payment_ref", None)
    if ref and check_payment_by_reference(ref):
        st.success("✅ Payment verified. You can now use the summarizer.")
        st.session_state.paid = True
    else:
        st.error("❌ Payment not verified. Please try again.")

def subscription_page():
    st.title("Subscription Plans")
    st.write("Choose your access plan to use the SmartDoc AI summarizer.")