import os
from pyrogram import Client, filters
from plugins.auth import SESSION_FILE, check_session

@Client.on_message(filters.command("session"))
def check_session_command(client, message):
    if check_session():
        message.reply_text("✅ Instagram session is active.")
    else:
        message.reply_text("⚠️ No active session. Use /login to log in.")

@Client.on_message(filters.command("clear_session"))
def clear_session(client, message):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        message.reply_text("✅ Session file deleted! Use /login to log in again.")
    else:
        message.reply_text("⚠️ No session file found.")
