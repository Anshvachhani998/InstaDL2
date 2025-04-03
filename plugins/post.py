import requests
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed
from database.db import db

app = Client

API_ENDPOINT = "https://instaapi-green.vercel.app/convert?url={}"
ADVANCE_API = "https://url-short-web.onrender.com/post?url={}"
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(p|reel|tv)/[^\s?]+)"

def fetch_instagram_data(url):
    """Fetch Instagram media (photo/video) from API"""
    try:
        response = requests.get(API_ENDPOINT.format(url))
        data = response.json()
        return data.get("dwn_url"), data.get("is_video")
    except Exception:
        return None, None

def fetch_advanced_data(url):
    """Alternative method to fetch Instagram media"""
    try:
        response = requests.get(ADVANCE_API.format(url))
        data = response.json()
        return data.get("media"), data.get("is_video")
    except Exception:
        return None, None

async def send_media(client, message, media_list, is_video, caption):
    """Send media content properly"""
    if len(media_list) == 1:  # Single file, send normally
        if is_video:
            await message.reply_video(media_list[0], caption=caption)
        else:
            await message.reply_photo(media_list[0], caption=caption)
    else:  # Multiple images, send one by one
        for media in media_list:
            await message.reply_photo(media)

async def download_content(client, message, url, user_id):
    """Download Instagram content"""
    downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Cᴏɴᴛᴇɴᴛ... 🎥**")

    media_url, is_video = fetch_instagram_data(url)
    
    if not media_url:  # Try alternative API
        await downloading_msg.edit("**⛔ Unable to fetch, trying backup method...**")
        media_url, is_video = fetch_advanced_data(url)
        
        if not media_url:
            await downloading_msg.edit("**⚠ Failed to fetch media. Account may be private.**")
            return
    
    caption = "**ʜᴇʀᴇ ɪꜱ Yᴏᴜʀ Cᴏɴᴛᴇɴᴛ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Bots**"
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/AnS_Bots")]])
    
    if isinstance(media_url, list):  # Multiple media (album)
        await send_media(client, message, media_url, is_video, caption)
    else:  # Single media
        if is_video:
            await message.reply_video(media_url, caption=caption, reply_markup=buttons)
        else:
            await message.reply_photo(media_url, caption=caption, reply_markup=buttons)

    # Log in dump channel
    await client.send_message(DUMP_CHANNEL, f"✅ **Downloaded by:** [{message.from_user.first_name}](tg://user?id={user_id})\n🔗 **URL:** {url}")
    await db.increment_download_count()
    await downloading_msg.delete()

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def handle_instagram_link(client, message):
    user_id = message.from_user.id
    url = message.matches[0].group(0)

    # ✅ Check if user is subscribed
    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        invite_link = await get_invite_link(client, FORCE_CHANNEL)
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Join Our Channel 🔥", url=invite_link)],
            [InlineKeyboardButton("🔓 I've Joined, Retry ✅", callback_data=f"check_sub#{user_id}#{url}")]
        ])
        return await message.reply(
            "**🔒 Access Denied!**\n\n"
            "🔹 To use this bot, you must join our update channel.\n"
            "🔹 After joining, press **'🔄 I've Joined'** to continue.",
            reply_markup=buttons
        )

    # Proceed to download
    await download_content(client, message, url, user_id)

@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id
    url = callback_query.data.split("#")[2]  # Extract URL

    if await is_subscribed(client, user_id, FORCE_CHANNEL):
        await callback_query.message.edit_text("✅ **Thanks for joining! Processing your request...**")
        await download_content(client, callback_query.message, url, user_id)
    else:
        await callback_query.answer("🚨 You are not subscribed yet!", show_alert=True)
