from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instagrapi import Client as InstaClient
import os
import re
import requests
import traceback  
import time  
from info import LOG_CHANNEL

INSTAGRAM_SESSION_FILE = "session.json"

insta_client = InstaClient()
if os.path.exists(INSTAGRAM_SESSION_FILE):
    insta_client.load_settings(INSTAGRAM_SESSION_FILE)
else:
    insta_client.login("harshvi_039", "Ansh123@123")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)

# ✅ Instagram Post URL Regex
INSTAGRAM_POST_REGEX = r"(https?:\/\/www\.instagram\.com\/p\/[A-Za-z0-9_-]+)"

def download_file(url, user_id, index, is_video):
    """✅ Download media with a unique filename"""
    timestamp = int(time.time())  
    ext = "mp4" if is_video else "jpg"
    filename = f"downloads/{user_id}_{index}_{timestamp}.{ext}"  

    os.makedirs("downloads", exist_ok=True)  

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            return filename  

    return None  

@Client.on_message(filters.regex(INSTAGRAM_POST_REGEX))  
def download_instagram_post(client, message):
    url = re.search(INSTAGRAM_POST_REGEX, message.text).group(0)  
    msg = message.reply_text("📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Pᴏꜱᴛ...")  
    
    try:
        media_pk = insta_client.media_pk_from_url(url)  
        media_info = insta_client.media_info(media_pk)  

        user_id = message.from_user.id
        first_name = message.from_user.first_name or "Unknown User"

        resources = media_info.resources if hasattr(media_info, "resources") else [media_info]

        file_paths = []  

        for index, resource in enumerate(resources):
            is_video = False
            file_path = None

            if resource.media_type == 2 and hasattr(resource, "video_url"):  # ✅ Video
                file_path = download_file(resource.video_url, user_id, index, is_video=True)
                is_video = True
            elif resource.media_type == 1 and hasattr(resource, "display_url"):  # ✅ Image
                file_path = download_file(resource.display_url, user_id, index, is_video=False)
            
            if file_path:
                file_paths.append((file_path, is_video))

        if file_paths:
            caption_user = "🖼 Hᴇʀᴇ ɪꜱ Yᴏᴜʀ Pᴏꜱᴛ 📩\n\nᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links"
            buttons_user = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔔 Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/Ans_Links")]
            ])

            caption_log = f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ:** **{message.from_user.mention}**\n📌 **Sᴏᴜʀᴄᴇ URL: [Cʟɪᴄᴋ Hᴇʀᴇ]({url})**"

            for file_path, is_video in file_paths:
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
                        caption=caption_log
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
                        caption=caption_log
                    )

                os.remove(file_path)  

        msg.delete()  

    except ValueError as ve:
        msg.edit_text(str(ve))
    except Exception as e:
        msg.edit_text("⚠ An error occurred while processing your request.")
        error_details = f"❌ **Error Log:**\n\n**User:** {first_name} (`{user_id}`)\n**URL:** {url}\n**Error:** `{str(e)}`\n\n```{traceback.format_exc()}```"
        client.send_message(LOG_CHANNEL, error_details)
