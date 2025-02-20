import os
import json
from pyrogram import Client, filters
from instagrapi import Client as InstaClient
from instagrapi.exceptions import LoginRequired, ChallengeRequired
from info import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

SESSION_FILE = "session.json"

# Initialize Instagram Client
cl = InstaClient()
cl.delay_range = [3, 6]  

# Function to check or login to Instagram
def login():
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.get_timeline_feed()
            return "✅ Logged in using session file."
        except LoginRequired:
            return "⚠️ Session expired. Please use /login to log in again."
    return "⚠️ No session found. Use /login to log in."


@Client.on_message(filters.command("login"))
def instagram_login(client, message):
    message.reply_text("🔄 Checking Instagram session...")

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.get_timeline_feed()
            message.reply_text("✅ Already logged in using session file.")
            return
        except LoginRequired:
            message.reply_text("⚠️ Session expired. Logging in again...")

    try:
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        cl.dump_settings(SESSION_FILE)
        message.reply_text("✅ Login successful! Session saved.")
    except ChallengeRequired:
        message.reply_text("⚠️ Instagram requires OTP. Check your email/SMS and use /otp <code> to proceed.")


@Client.on_message(filters.command("otp"))
def handle_otp(client, message):
    otp_code = message.text.split(" ", 1)[-1].strip()
    if not otp_code.isdigit() or len(otp_code) != 6:
        message.reply_text("❌ Invalid OTP. Please enter a 6-digit OTP like: `/otp 123456`")
        return

    try:
        cl.challenge_code_handler = lambda username, choice: otp_code
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        cl.dump_settings(SESSION_FILE)
        message.reply_text("✅ OTP verified, login successful!")
    except Exception as e:
        message.reply_text(f"❌ OTP failed: {str(e)}")


@Client.on_message(filters.command("session"))
def check_session(client, message):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            session_data = json.load(f)
        session_info = json.dumps(session_data, indent=2)[:4000]  # Telegram message limit
        message.reply_text(f"📄 **Session Info:** {session_info}")
    else:
        message.reply_text("⚠️ No session file found. Please log in using /login.")


@Client.on_message(filters.command("clear_session"))
def clear_session(client, message):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        message.reply_text("✅ Session file deleted! Use /login to log in again.")
    else:
        message.reply_text("⚠️ No session file found.")
      
