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

video_map = {}

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
    video_link = None
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        video = request.files['video']
        if video.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if video and video.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            original_filename = video.filename
            unique_id = str(uuid.uuid4())
            unique_filename = f"{unique_id}_{original_filename}"
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            video_map[unique_id] = unique_filename

            video_link = url_for('video_redirect', unique_id=unique_id, _external=True)
            print(f'Generated video link: {video_link}')  # Debugging statement
            flash(f'Video uploaded successfully! Here is your link: {video_link}', 'success')

    videos = [filename for filename in os.listdir(app.config['UPLOAD_FOLDER']) if filename.split('_')[0] in video_map]
    return render_template('admin_dashboard.html', videos=videos, video_link=video_link)

@app.route('/uploads/<unique_id>')
def serve_video(unique_id):
    filename = video_map.get(unique_id)
    if not filename:
        return "Video not found", 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video/<unique_id>')
def video_redirect(unique_id):
    return redirect(url_for('watch_ad', unique_id=unique_id))

@app.route('/watch/<unique_id>')
def watch_ad(unique_id):
    video_url = url_for('serve_video', unique_id=unique_id, _external=True)
    return render_template('index.html', video_url=video_url)

@app.route('/skip-ad', methods=['POST'])
def skip_ad():
    video_url = request.form.get('video_url')
    if video_url:
        return redirect(video_url)
    else:
        return "No video URL provided", 400
    
@app.route('/play-video')
def play_video():
    video_url = request.args.get('video_url')
    return render_template('video.html', video_url=video_url)

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

    unique_id = str(uuid.uuid4())  # Generating a unique ID for the user request
    video_redirect_url = url_for('video_redirect', unique_id=unique_id, _external=True)
    await update.message.reply_text(f"Watch the video here: {video_redirect_url}")
def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_video", send_video))

    loop.run_until_complete(application.run_polling())

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    app.run(debug=True)
