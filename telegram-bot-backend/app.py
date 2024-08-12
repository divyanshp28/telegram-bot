from flask import Flask, request, jsonify
import telebot

app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

@app.route('/start', methods=['GET'])
def start():
    user_id = request.args.get('user_id')
    if user_id:
        bot.send_message(user_id, "Welcome to the bot! Please watch this ad.")
        # Send a message with the ad content (you can customize this)
        bot.send_message(user_id, "Ad Content: [Skip Ad](http://your-angular-app-url/ad)", parse_mode="Markdown")
    return jsonify({"status": "success"})

@app.route('/skip_ad', methods=['GET'])
def skip_ad():
    user_id = request.args.get('user_id')
    if user_id:
        bot.send_message(user_id, "Here is your video: [Watch Video](http://your-angular-app-url/bot)", parse_mode="Markdown")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
