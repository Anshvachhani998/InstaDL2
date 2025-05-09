from pyrogram import Client, filters
from instagrapi import Client as InstaClient

from database.db import db

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


from pyrogram import Client, filters
from instagrapi import Client as InstaClient

# Instagram client setup
insta_client = InstaClient()

# Load saved session (assuming you already have a load_session() function)
@Client.on_message(filters.command("reel") & filters.private)
async def get_reel_info(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Please provide a Reel URL.\n\nUsage: `/reel <reel_url>`", quote=True)

    reel_url = message.text.split(" ", 1)[1].strip()


    try:
        media_id = insta_client.media_pk_from_url(reel_url)
        reel_info = insta_client.media_info(media_id)

        video_url = str(reel_info.video_url)
        await message.reply_text(f"🎬 **Reel Video URL:**\n{video_url}")
    except Exception as e:
        await message.reply_text(f"❌ Failed to fetch reel info:\n{e}")
