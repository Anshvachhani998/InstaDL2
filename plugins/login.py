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

async def fetch_post(post_url: str):
    try:
        # Extract media ID from the post URL
        media_id = insta.media_pk_from_url(post_url)
        
        # Fetch media information (which includes images, videos, etc.)
        post_info = insta.media_info(media_id)
        
        # Check if it's a carousel (multiple images/videos)
        if post_info.resources:
            media_urls = []
            for resource in post_info.resources:
                media_url = resource.video_url if resource.video_url else resource.thumbnail_url
                media_urls.append(str(media_url))  # Convert URL to string

            return media_urls

        else:
            # If it's a single image/video post, return its URL
            media_url = post_info.video_url if post_info.video_url else post_info.thumbnail_url
            return [str(media_url)]  # Return as a list with a single URL

    except Exception as e:
        return f"❌ Failed to fetch post info: {str(e)}"

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
