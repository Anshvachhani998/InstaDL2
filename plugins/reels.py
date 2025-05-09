import random
import os
import asyncio
import subprocess
import re
import requests
import traceback  
import time
import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed
from database.db import db
from asyncio import create_task
from plugins.login import fetch_reel

app = Client

API_ENDPOINT = "https://instaapi-green.vercel.app/convert?url={}"
ADVANCE_API = "https://instadl-api.koyeb.app/reel?url={}"
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(share/)?reel/[^\s?]+)"


def download_file(url, user_id):
    """✅ Download reel with a unique filename"""
    timestamp = int(time.time())  
    filename = f"downloads/{user_id}_{timestamp}.mp4"  

    os.makedirs("downloads", exist_ok=True)  

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            return filename  

    return None  
    
async def advance_fatch_url(instagram_url):
    """API endpoint se direct media URL fetch karega"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ADVANCE_API.format(instagram_url)) as response:
                data = await response.json()
                return data.get("video_url")
    except Exception:
        return None
        
async def advance_content(client, message, url, user_id, mention=None):
    """Function to download the Instagram content"""
    try:
        downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷**")
        
        video_url = await fetch_reel(url)
        if not video_url:
            await downloading_msg.edit(
                "** 🚫 Unable to retrieve publication information.**\n\n"
                "This could be due to the following reasons:\n"
                "▫️ The account is private or closed.\n"
                "▫️ A data retrieval error occurred.\n"
                "▫️ The content might be restricted due to age or copyright limitations.\n\n"
                "⚠ **If the issue persists, please inform the admin or ask for help in our support group.**\n\n"
                "**💬 Support Group: [SUPPORT](https://t.me/AnSBotsSupports)**",
                disable_web_page_preview=True
            )
            error_message = f"**Error**\n **{url}**\n⚠️ Rᴇᴇʟꜱ Nᴏᴛ Fᴏᴜɴᴅ"
            await client.send_message(LOG_CHANNEL, error_message)           
            return
        
        caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Rᴇᴇʟꜱ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Bots**"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/AnS_Bots")]
        ])

        await message.reply_video(video_url, caption=caption_user, reply_markup=buttons)

        # `mention` ko check karenge, agar None hai toh `message.from_user.mention` use karenge
        user_mention = mention or message.from_user.mention  

        await client.send_video(DUMP_CHANNEL, video=video_url, caption=f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ: {user_mention}**\n📌 **Sᴏᴜʀᴄᴇ URL: [Click Here]({url})**")
        await db.increment_download_count()
        await downloading_msg.delete()

    except Exception as e:
        try:
            # Re-try downloading and uploading the video again
            file_path = download_file(video_url, user_id)

            if file_path:
                # Re-attempt sending the video
                caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Rᴇᴇʟꜱ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʏʙ @Ans_Bots**"
                buttons_user = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/AnS_Bots")]
                ])

                # Sending the video to the user again
                await client.send_video(
                    chat_id=message.chat.id,
                    video=file_path,
                    caption=caption_user,
                    reply_markup=buttons_user,
                    reply_to_message_id=message.id
                )

                # Preparing the log message and sending to dump channel again
                user_mention = mention or message.from_user.mention
                caption_log = f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ:** **{user_mention}**\n📌 **Sᴏᴜʀᴄᴇ URL: [Cʟɪᴄᴋ Hᴇʀᴇ]({url})**"
                await client.send_video(DUMP_CHANNEL, video=file_path, caption=caption_log)

                # Increment download count in DB
                await db.increment_download_count()

                # Deleting the downloading message after retry
                await downloading_msg.delete()
            else:
                # If retry fails, update the downloading message
                await downloading_msg.edit("🚨 **Failed to download video on retry.** Please contact support.")
                error_message = f"**Error**\n **{url}**\n⚠️ Video download failed on retry"
                await client.send_message(LOG_CHANNEL, error_message)

        except Exception as retry_error:
            # If retry fails, log the retry error and notify the user
            retry_error_message = f"🚨 **Retry Error Alert!**\n\n🔹 **User:** {mention or message.from_user.mention}\n🔹 **URL:** {url}\n🔹 **Retry Error:** `{retry_error}`"
            await client.send_message(LOG_CHANNEL, retry_error_message)
            await message.reply(f"**⚠ Something went wrong. Please contact [ADMIN](https://t.me/AnS_team) for support.**")
            


@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def handle_instagram_link(client, message):
    user_id = message.from_user.id
    url = message.matches[0].group(0)

    create_task(advance_content(client, message, url, user_id))


@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id  # Correct user ID
    mention = callback_query.from_user.mention  # Correct user mention
    url = callback_query.data.split("#")[2]  # Extract URL from callback data
    
    if await is_subscribed(client, user_id, FORCE_CHANNEL):
        an = await callback_query.message.edit_text("**🙏 Tʜᴀɴᴋs Fᴏʀ Jᴏɪɴɪɴɢ! Nᴏᴡ Pʀᴏᴄᴇssɪɴɢ Yᴏᴜʀ Lɪɴᴋ...**")

        await advance_content(client, callback_query.message, url, user_id, mention)
        await an.delete()
    else:
        await callback_query.answer("🚨 You are not subscribed yet!", show_alert=True)
