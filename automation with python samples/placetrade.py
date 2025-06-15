import websocket
import json
import time

# Define WebSocket URL
app_id = "728617382"  # Use your app_id
ws_url = ws_url = "wss://ws.binaryws.com/websockets/v3"


def on_message(ws, message):
    print("Trade Response:", message)

def on_open(ws):
    print("Connected to Deriv WebSocket!")

    # Prepare trade request
    trade_request = {
        "buy": 1,
        "price": 100,  # Adjust price accordingly
        "symbol": "R_50",  # Use a valid Deriv symbol
        "duration": 60,
        "duration_unit": "s",
        "contract_type": "CALL",
        "currency": "USD"
    }

    # Send trade request after a short delay
    time.sleep(2)
    ws.send(json.dumps(trade_request))
    print("Trade request sent!")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed.")

# Create WebSocket connection
ws = websocket.WebSocketApp(ws_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()
# To get the actual app_id, you need to register an application on the Deriv website.
# Visit https://app.deriv.com/account/api-apps to create a new application and get your app_id.