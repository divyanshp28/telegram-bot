from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BOT_TOKEN = 'YOUR_BOT_TOKEN'  

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    webhook_url = request.json.get('webhook_url')
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    chat_id = data['message']['chat']['id']

    send_message(chat_id, "Click this link to view the ad: https://your-angular-app.com/ad")

    return jsonify({"status": "success"})

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
