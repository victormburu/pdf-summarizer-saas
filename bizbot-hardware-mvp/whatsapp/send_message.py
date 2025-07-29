import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp(to: str, message: str) -> str:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp_number = f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
    
    client = Client(account_sid, auth_token)
    
    msg = client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=f"whatsapp:{to}"
    )
    
    return  msg.sid