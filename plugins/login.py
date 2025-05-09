import asyncio
import re 
from pyrogram import Client, filters
from instagrapi import Client as InstaClient
from database.db import db

insta = InstaClient()


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

    try:
        insta.login("loveis8507", "Ansh12345@23")
        session_data = insta.get_settings()
        await db.save_session(session_data)
        await message.reply_text("🔐 Logged in and session saved to DB.")
    except Exception as e:
        await message.reply_text(f"❌ Login failed: {str(e)}")

async def fetch_reel(reel_url: str):
    try:
        media_id = await asyncio.to_thread(insta.media_pk_from_url, reel_url)
        reel_info = await asyncio.to_thread(insta.media_info, media_id)
        
        video_url = str(reel_info.video_url)
        return video_url

    except Exception as e:
        return f"❌ Failed to fetch reel info: {str(e)}"

async def fetch_stories(story_url: str):
    try:
        match = re.search(r"/stories/[^/]+/(\d+)", story_url)
        if not match:
            return "❌ Invalid story URL format"
            
        story_id = match.group(1)
        story_info = await asyncio.to_thread(insta.media_info, story_id)

        media_url = story_info.video_url if story_info.video_url else story_info.thumbnail_url
        
        return str(media_url)

    except Exception as e:
        return f"❌ Failed to fetch story info: {str(e)}"

async def fetch_caption(insta_url: str):
    try:
        media_id = await asyncio.to_thread(insta.media_pk_from_url, insta_url)
        media_info = await asyncio.to_thread(insta.media_info, media_id)
        return media_info.caption_text or "No caption available."

    except Exception as e:
        return f"❌ Failed to fetch caption: {str(e)}"

async def fetch_user_profile(username: str):
    try:
        user_info = await asyncio.to_thread(insta_client.user_info_by_username_v1, username)

        return {
            "full_name": user_info.full_name or "No name available.",
            "profile_pic": str(user_info.profile_pic_url_hd),
            "bio": user_info.biography or "No bio available.",
            "followers": user_info.follower_count,
            "following": user_info.following_count,
            "is_private": user_info.is_private,
            "is_verified": user_info.is_verified,
        }

    except Exception as e:
        return {"error": f"❌ Failed to fetch user info: {str(e)}"}

async def fetch_post(post_url: str):
    try:
        # Run the blocking calls in a separate thread
        media_id = await asyncio.to_thread(insta.media_pk_from_url, post_url)
        post_info = await asyncio.to_thread(insta.media_info, media_id)

        # If it's a carousel (multiple media)
        if post_info.resources:
            media_urls = []
            for resource in post_info.resources:
                media_url = resource.video_url if resource.video_url else resource.thumbnail_url
                media_urls.append(str(media_url))
            return media_urls
        else:
            media_url = post_info.video_url if post_info.video_url else post_info.thumbnail_url
            return [str(media_url)]

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
