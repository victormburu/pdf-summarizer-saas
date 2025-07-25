
from twilio.rest import Client

account_sid = 'AC0d701d5ec7c4f6f9523c890a5d0f9b30'
auth_token = 'c0ddaeadac6bc144656a4b86bfc11385'
client = Client(account_sid, auth_token)

message = client.messages.create(
    to='+18777804236',
    from_='+16402234548',
    body='hey lad, am proud of you'
)

print(f"Message SID: {message.sid}, Status: {message.status}")
