# webhook.py
from flask import Flask, request, jsonify
import hmac
import hashlib
import json
from firebase_config import db

app = Flask(__name__)

PAYSTACK_SECRET = "sk_live_6e48515cf6846919c9a75c01c37de32922b63ce6"

@app.route('/paystack-webhook', methods=['POST'])
def paystack_webhook():
    payload = request.data
    received_sig = request.headers.get('x-paystack-signature')

    # Verify signature
    expected_sig = hmac.new(
        key=PAYSTACK_SECRET.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha512
    ).hexdigest()

    if received_sig != expected_sig:
        return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400

    data = json.loads(payload)

    # 📦 Handle payment confirmation
    if data['event'] == 'charge.success':
        email = data['data']['customer']['email']
        reference = data['data']['reference']
        amount = data['data']['amount'] / 100  # convert from kobo to KES

        print(f"✅ Payment successful for {email}, {amount} KES, ref: {reference}")

        # TODO: mark this email as paid in your DB
        mark_user_paid(email, reference, amount)

    return jsonify({'status': 'success'}), 200

def mark_user_paid(email, reference, amount):
    user_ref = db.collection("paid_users").document(email)
    user_ref.set({
        "email": email,
        "reference": reference,
        "amount": amount,
        "status": "paid"
    })
    

if __name__ == '__main__':
    app.run(port=8000)
