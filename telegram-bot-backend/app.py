import asyncio
import os
from flask import Flask, request, redirect, send_from_directory, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploaded_videos'

ADMIN_EMAIL = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin'

# Telegram bot token
BOT_TOKEN = '7159342226:AAHEdFVDm1DhfNZ779biG2QMBMSVwncklfM'

# Web app URL
WEB_APP_URL = 'https://telegram-bot-aagw.onrender.com/'  # Public URL of the hosted Flask service

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login' 

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Admin(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return Admin(id="admin")
    return None

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            admin_user = Admin(id="admin")
            login_user(admin_user)
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('admin_login.html')

@app.route('/admin-logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have successfully logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        video = request.files['video']
        if video.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if video and video.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            filename = video.filename
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Video uploaded successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid file type. Only video files are allowed.', 'danger')

    videos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('admin_dashboard.html', videos=videos)

@app.route('/uploads/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    # Render the ad page
    return render_template('index.html')

@app.route('/video/<filename>')
def video_redirect(filename):
    video_url = url_for('serve_video', filename=filename, _external=True)
    return redirect(f"{WEB_APP_URL}?video_url={video_url}")

@app.route('/skip-ad', methods=['POST'])
def skip_ad():
    video_url = request.args.get('video_url') 
    if video_url:
        return redirect(video_url)
    else:
        return "No video URL provided", 400

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Watch Ad", url=WEB_APP_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click the button below to watch an ad. After the ad, you will see the main video.",
        reply_markup=reply_markup
    )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a video filename.")
        return

    video_filename = context.args[0]
    video_redirect_url = url_for('video_redirect', filename=video_filename, _external=True)
    await update.message.reply_text(f"Watch the video here: {video_redirect_url}")

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
