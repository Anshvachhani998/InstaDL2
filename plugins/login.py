from pyrogram import Client, filters
from instagrapi import Client as InstaClient



# Pyrogram command for login
@Client.on_message(filters.command("login"))
async def insta_login_handler(client, message):
    insta = InstaClient()

    # Load session from DB
    session_data = await load_session()

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
        await save_session(session_data)  # Save session to DB
        await message.reply_text("🔐 Logged in and session saved to DB.")
    except Exception as e:
        await message.reply_text(f"❌ Login failed: {str(e)}")
