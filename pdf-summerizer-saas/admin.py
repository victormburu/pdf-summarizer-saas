import smtplib
from email.message import EmailMessage
import streamlit as st

# Dummy users list for demonstration
users = [
    {"email": "user1@example.com", "status": "active"},
    {"email": "user2@example.com", "status": "disabled"},
    {"email": "user3@example.com", "status": "active"},
]

def notify_admin_disabled_user(email):
    msg = EmailMessage()
    msg['Subject'] = 'Disabled User Login Attempt'
    msg['From'] = 'yourapp@gmail.com'
    msg['To'] = 'victormburu30@gmail.com'
    msg.set_content(f'User with email {email} attempted to log in but is disabled.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('yourapp@gmail.com', 'your_app_password')
        smtp.send_message(msg)
