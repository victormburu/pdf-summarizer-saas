import requests

url = "https://api.deriv.com/v2/ticks/BTCUSD"
response = requests.get(url)
data = response.json()
print(f"Latest BTC Price: {data['tick']['quote']}")




