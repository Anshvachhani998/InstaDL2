from pyrogram import Client, filters
from instagrapi import Client as InstaClient

from database.db import db

insta = InstaClient()

# Pyrogram command for login
@Client.on_message(filters.command("login"))
async def insta_login_handler(client, message):
    insta = InstaClient()

    # Load session from DB
    session_data = await db.load_session()

    if session_data:
        insta.set_settings(session_data)
        try:
            insta.get_timeline_feed()
            await message.reply_text("✅ Session loaded from DB and is valid.")
            return
        except Exception as e:
            await message.reply_text("⚠️ Session expired or invalid. Logging in again...")

    # If no session or expired, login and save
    try:
        insta.login("loveis8507", "Ansh12345@23")  # Don't hardcode in real use
        session_data = insta.get_settings()
        await db.save_session(session_data)  # Save session to DB
        await message.reply_text("🔐 Logged in and session saved to DB.")
    except Exception as e:
        await message.reply_text(f"❌ Login failed: {str(e)}")

async def fetch_reel(reel_url: str):
    try:
        media_id = insta.media_pk_from_url(reel_url)
        reel_info = insta.media_info(media_id)
        video_url = str(reel_info.video_url)
        
        return video_url
    except Exception as e:
        return f"❌ Failed to fetch reel info: {str(e)}"


async def auto_login():
    session_data = await db.load_session()

    if session_data:
        insta.set_settings(session_data)
        try:
            insta.get_timeline_feed()
            print("✅ Session loaded from DB and is valid.")
            return insta
        except Exception as e:
            print("⚠️ Session expired. Logging in again...")

    try:
        insta.login("loveis8507", "Ansh12345@23")  # 🔐 Use env in production
        session_data = insta.get_settings()
        await db.save_session(session_data)
        print("🔐 Logged in and session saved to DB.")
        return insta
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return None
