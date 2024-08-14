# from flask import Flask, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/video', methods=['GET'])
# def get_video():
#     return jsonify({
#         'ad_video_url': 'https://www.youtube.com/embed/rXzfcLIzGQU',
#         'main_video_url': 'https://www.youtube.com/embed/51QV0v8GGbM'
#     })

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, request
from flask_cors import CORS
import telebot

# Flask setup
app = Flask(__name__)
CORS(app)

# Telegram bot setup
API_TOKEN = '7159342226:AAHEdFVDm1DhfNZ779biG2QMBMSVwncklfM'
bot = telebot.TeleBot(API_TOKEN)

video_data = {
    'ad_video_url': 'https://www.youtube.com/embed/rXzfcLIzGQU',
    'main_video_url': 'https://www.youtube.com/embed/51QV0v8GGbM'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Welcome! Click the link to watch an ad. After skipping, the main video will start. Visit our site: https://telegram-bot-video.onrender.com"
    )
    send_ad(message)


def send_ad(message):
    markup = telebot.types.InlineKeyboardMarkup()
    skip_button = telebot.types.InlineKeyboardButton(text="Skip Ad", callback_data="skip")
    close_button = telebot.types.InlineKeyboardButton(text="Close Ad", callback_data="close")
    markup.add(skip_button, close_button)

    bot.send_message(
        message.chat.id,
        f"Watch this ad: {video_data['ad_video_url']}",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data in ["skip", "close"])
def handle_callback(call):
    if call.data == "skip":
        bot.send_message(
            call.message.chat.id,
            f"Ad skipped! Now playing: {video_data['main_video_url']}"
        )
    elif call.data == "close":
        bot.send_message(
            call.message.chat.id,
            "Ad closed. No video will be played."
        )

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

if __name__ == '__main__':
    bot.remove_webhook()
    # frontend url deployed on netlify
    bot.set_webhook(url="https://telegram-bot-r3bg.onrender.com/webhook")
    app.run(debug=True)

