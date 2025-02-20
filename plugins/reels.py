from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instagrapi import Client as InstaClient
import os
import re
import requests
import traceback  
from info import LOG_CHANNEL

INSTAGRAM_SESSION_FILE = "session.json"

insta_client = InstaClient()
if os.path.exists(INSTAGRAM_SESSION_FILE):
    insta_client.load_settings(INSTAGRAM_SESSION_FILE)
else:
    insta_client.login("harshvi_039", "Ansh123@123")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)

INSTAGRAM_LINK_REGEX = r"(https?:\/\/www\.instagram\.com\/(?:p|reel|tv)\/[A-Za-z0-9_-]+)"

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return filename
    return None

@Client.on_message(filters.regex(INSTAGRAM_LINK_REGEX))  
def download_instagram_media(client, message):
    url = re.search(INSTAGRAM_LINK_REGEX, message.text).group(0)  
    msg = message.reply_text("Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷")  

    try:
        media_pk = insta_client.media_pk_from_url(url)  
        media_info = insta_client.media_info(media_pk)  
        
        file_path = None
        is_video = False  # ✅ Track media type

        if media_info.video_url:
            file_path = download_file(media_info.video_url, "video.mp4")
            is_video = True
        elif media_info.thumbnail_url:
            file_path = download_file(media_info.thumbnail_url, "photo.jpg")
        else:
            raise ValueError("⚠ No media found in this post.")  

        if file_path:
            first_name = message.from_user.first_name if message.from_user.first_name else "Unknown User"
            user_id = message.from_user.id
            
            caption_user = "ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ᴠɪᴅᴇᴏ 🎥\n\nᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links"
            buttons_user = InlineKeyboardMarkup([
                [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/Ans_Links")]
            ])

            caption_dump = f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ:** {first_name} (Telegram ID: `{user_id}`)\n📌 **Sᴏᴜʀᴄᴇ URL:** [Cʟɪᴄᴋ Hᴇʀᴇ]({url})"

            # ✅ Send media to user
            if is_video:
                client.send_video(
                    chat_id=message.chat.id,
                    video=file_path,
                    caption=caption_user,
                    reply_markup=buttons_user,
                    reply_to_message_id=message.id
                )
                client.send_video(
                    chat_id=LOG_CHANNEL,
                    video=file_path,
                    caption=caption_dump
                )
            else:
                client.send_photo(
                    chat_id=message.chat.id,
                    photo=file_path,
                    caption=caption_user,
                    reply_markup=buttons_user,
                    reply_to_message_id=message.id
                )
                client.send_photo(
                    chat_id=LOG_CHANNEL,
                    photo=file_path,
                    caption=caption_dump
                )

            os.remove(file_path)
        
        msg.delete()  

    except ValueError as ve:
        msg.edit_text(str(ve))
    except Exception as e:
        msg.edit_text("⚠ An error occurred while processing your request.")
        error_details = f"❌ **Error Log:**\n\n**User:** {message.from_user.mention} (`{message.from_user.id}`)\n**URL:** {url}\n**Error:** `{str(e)}`\n\n```{traceback.format_exc()}```"
        client.send_message(LOG_CHANNEL, error_details)
