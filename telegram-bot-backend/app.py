import asyncio
from flask import Flask, render_template, request, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

app = Flask(__name__)

# Telegram bot token
BOT_TOKEN = '7159342226:AAHEdFVDm1DhfNZ779biG2QMBMSVwncklfM'

# Web app URL (update this when you deploy)
WEB_APP_URL = 'http://127.0.0.1:5000/'  # Localhost for testing

@app.route('/')
def index():
    # Render the ad page
    return render_template('index.html')

@app.route('/skip-ad', methods=['POST'])
def skip_ad():
    # After the ad is skipped, render the video page
    return render_template('video.html')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Watch Ad", url=WEB_APP_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click the button below to watch an ad. After the ad, you will see the main video.",
        reply_markup=reply_markup
    )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_url = "https://www.youtube.com/embed/vZtm1wuA2yc"  # Replace with your video URL
    await update.message.reply_text(f"Here is your video: {video_url}")

def run_bot():
    # Create a new event loop for this thread
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    # Initialize the Application (bot)
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_video", send_video))

    # Run the bot
    loop.run_until_complete(application.run_polling())

if __name__ == '__main__':
    # Run the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Run the Flask app
    app.run(debug=True)
