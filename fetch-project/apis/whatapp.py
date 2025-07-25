from twilio.rest import Client

account_sid = 'AC0d701d5ec7c4f6f9523c890a5d0f9b30'
auth_token = 'c0ddaeadac6bc144656a4b86bfc11385'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HX229f5a04fd0510ce1b071852155d3e75',
  content_variables='{"1":"328618"}',
  to='whatsapp:+254782699338'
)

print(message.sid)
