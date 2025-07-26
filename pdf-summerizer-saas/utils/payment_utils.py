import requests
import uuid
import streamlit as st
from firebase_config import db

PAYSTACK_SECRET_KEY = "sk_live_6e48515cf6846919c9a75c01c37de32922b63ce6"
PAYSTACK_BASE_URL = "https://api.paystack.co"

def create_payment_link(email, plan, provider):
    if provider == "paypal":
        paypal_links = {
            "Daily - KES 50": "https://paypal.com/paypal-daily50",
            "Weekly - KES 200": "https://paypal.com/paypal-weekly200",
            "Monthly - KES 500": "https://paypal.com/paypal-monthly500"
        }
        return paypal_links.get(plan)

    # Dynamically create Paystack payment for African users
    amount_map = {
        "Daily - KES 50": 50 * 100,
        "Weekly - KES 200": 200 * 100,
        "Monthly - KES 500": 500 * 100
    }

    reference = str(uuid.uuid4())  # Generate a unique reference
    amount = amount_map.get(plan, 50000)  # Default KES 500

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    #reference = generate_transaction_ref()
    email = "payment@smartdoc.ai"
    payload = {
        "email": email,
        "amount": amount,
        "reference": reference,
        "currency": "KES",
        "callback_url": "https://yourdomain.com/payment-callback"  # optional
    }

    try:
        res = requests.post(f"{PAYSTACK_BASE_URL}/transaction/initialize", json=payload, headers=headers)
        data = res.json()

        if data['status']:
            payment_url = data['data']['authorization_url']
            # Store reference in session so it can be used during verification
            st.session_state["payment_ref"] = reference
            return payment_url
        else:
            raise Exception(data['message'])

    except Exception as e:
        print(f"Failed to create Paystack payment: {e}")
        return None

def check_payment_by_reference(reference):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.get(f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}", headers=headers)
        data = res.json()

        if data['status'] and data['data']['status'] == "success":
            return True
        else:
            return False
    except Exception as e:
        print(f"Verification failed: {e}")
        return False


def check_payment_status(email):
    try:
        user_ref = db.collection("paid_users").document(email).get()
        if user_ref.exists and user_ref.to_dict().get("status") == "paid":
            return True
    except Exception as e:
        print(f"Error checking payment: {e}")
    return False
