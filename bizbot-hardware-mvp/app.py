#flask server
from flask import request
import flask
from whatsapp.message_processor import handle_message

app = flask.Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    response = handle_message(data)
    return response, 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)