import os
import json
from pyrogram import Client, filters
from plugins.auth import SESSION_FILE

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
