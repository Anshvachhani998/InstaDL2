from pyrogram import Client, filters
from plugins.auth import insta_client, login

@Client.on_message(filters.command("login"))
def instagram_login(client, message):
    message.reply_text("🔄 Checking Instagram session...")
    response = login()  # `auth.py` ka login function use kar rahe hain
    message.reply_text(response)
  
