import uuid
import os
import requests
import streamlit as st
from firebase_config import db
from dotenv import load_dotenv
from firebase_admin import firestore

load_dotenv()
# Config
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")  # or hardcode for testing
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYSTACK_BASE_URL = os.getenv("PAYSTACK_BASE_URL")
PAYPAL_BASE_URL ="https://api-m.paypal.com"

# Main payment link creator
def create_payment_link(email, amount, plan, provider):
    EXCHANGE_RATE = 150  # 🔁 KES to USD (update as needed)
    db = firestore.client()  # 🧠 Ensure Firebase Admin is initialized

    if provider.lower() == "paypal":
        paypal_prices_usd = {
            "Daily - KES 50": round((50 * 2) / EXCHANGE_RATE, 2),
            "Weekly - KES 200": round((200 * 2) / EXCHANGE_RATE, 2),
            "Monthly - KES 500": round((500 * 2) / EXCHANGE_RATE, 2)
        }

        amount = paypal_prices_usd.get(plan, 5.00)
        currency = "USD"

        # Step 1: Get PayPal Access Token
        token_resp = requests.post(
            f"{os.getenv('PAYPAL_BASE_URL')}/v1/oauth2/token",
            auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_SECRET")),
            headers={"Accept": "application/json"},
            data={"grant_type": "client_credentials"}
        )

        if token_resp.status_code != 200:
            print("❌ Failed to authenticate with PayPal:", token_resp.text)
            return None

        access_token = token_resp.json().get("access_token")

        # Step 2: Create PayPal Order
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        order_payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                }
            }],
            "application_context": {
                "return_url": "https://pdf-summarize-saas-3io2cffcxnp6cpkhvhoxip.streamlit.app/payment-success",
                "cancel_url": "https://pdf-summarize-saas-3io2cffcxnp6cpkhvhoxip.streamlit.app/payment-cancel"
            }
        }

        order_resp = requests.post(
            f"{os.getenv('PAYPAL_BASE_URL')}/v2/checkout/orders",
            headers=headers,
            json=order_payload
        )

        if order_resp.status_code != 201:
            print("❌ Failed to create PayPal order:", order_resp.text)
            return None

        order_data = order_resp.json()
        approval_url = next((link["href"] for link in order_data["links"] if link["rel"] == "approve"), None)
        order_id = order_data["id"]

        if approval_url:
            db.collection("payments").document(order_id).set({
                "email": email,
                "plan": plan,
                "amount": amount,
                "currency": currency,
                "provider": "PayPal",
                "payment_ref": order_id,
                "status": "pending"
            })

            return approval_url
        else:
            print("❌ Approval URL not found.")
            return None

    elif provider.lower() == "paystack":
        amount_map = {
            "Daily - KES 50": 50 * 100,
            "Weekly - KES 200": 200 * 100,
            "Monthly - KES 500": 500 * 100
        }

        amount = amount_map.get(plan, 50000)
        reference = str(uuid.uuid4())

        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "email": email,
            "amount": amount,
            "reference": reference,
            "currency": "KES",
            "callback_url": "https://pdf-summarize-saas-3io2cffcxnp6cpkhvhoxip.streamlit.app/payment-callback"
        }

        try:
            res = requests.post(f"{os.getenv('PAYSTACK_BASE_URL')}/transaction/initialize", json=payload, headers=headers)
            data = res.json()
            if data['status']:
                st.session_state["payment_ref"] = reference
                db.collection("payments").document(reference).set({
                    "email": email,
                    "plan": plan,
                    "amount": amount / 100,  # Convert back to normal for Firebase
                    "currency": "KES",
                    "provider": "Paystack",
                    "payment_ref": reference,
                    "status": "pending"
                })
                return data['data']['authorization_url']
            else:
                raise Exception(data['message'])
        except Exception as e:
            print(f"❌ Paystack error: {e}")
            return None

    else:
        print("❌ Unknown payment provider.")
        return None

def check_payment_status(transaction_id, provider):
    if provider == "Paystack":
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        }
        url = f"https://api.paystack.co/transaction/verify/{transaction_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["status"] == "success"
        else:
            return False

    elif provider == "PayPal":
        # Step 1: Get Access Token
        auth_response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
            headers={"Accept": "application/json"},
            data={"grant_type": "client_credentials"},
        )
        if auth_response.status_code != 200:
            return False
        access_token = auth_response.json()["access_token"]
        # Step 2: Check Order Status
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        order_url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{transaction_id}/order"
        order_response = requests.get(order_url, headers=headers)

        if order_response.status_code == 201:
            order_data = order_response.json()
            status = order_data.get("status")
            if status == "COMPLETED":
                db.collection("payments").document(transaction_id).update({"status": "COMPLETED"})
                return True
            return False

    return False
