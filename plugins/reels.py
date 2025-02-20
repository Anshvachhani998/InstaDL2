from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instagrapi import Client as InstaClient
import os
import re
import requests

# Initialize Instagram Client
INSTAGRAM_SESSION_FILE = "session.json"
insta_client = InstaClient()

# Load session if exists
if os.path.exists(INSTAGRAM_SESSION_FILE):
    insta_client.load_settings(INSTAGRAM_SESSION_FILE)
else:
    insta_client.login("harshvi_039", "Ansh123@123")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)

# ✅ Instagram link detect karne ke liye regex
INSTAGRAM_LINK_REGEX = r"(https?:\/\/www\.instagram\.com\/(?:p|reel|tv)\/[A-Za-z0-9_-]+)"

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return filename
    return None

@Client.on_message(filters.regex(INSTAGRAM_LINK_REGEX))  # ✅ Jab koi Instagram link send kare
def download_instagram_media(client, message):
    url = re.search(INSTAGRAM_LINK_REGEX, message.text).group(0)  # ✅ Extract Instagram link
    msg = message.reply_text("Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷")  # ✅ Show downloading message

    try:
        media_pk = insta_client.media_pk_from_url(url)  # ✅ Get media_pk
        media_info = insta_client.media_info(media_pk)  # ✅ Get media details
        
        file_path = None
        if media_info.video_url:
            file_path = download_file(media_info.video_url, "video.mp4")
            send_function = message.reply_video
        elif media_info.thumbnail_url:
            file_path = download_file(media_info.thumbnail_url, "photo.jpg")
            send_function = message.reply_photo
        else:
            msg.edit_text("⚠ No media found in this post.")
            return

        if file_path:
            # ✅ Caption & Button
            caption = "ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ᴠɪᴅᴇᴏ 🎥\n\n ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links"
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/Ans_Links")]
            ])
            
            # ✅ Send media
            send_function(file_path, caption=caption, reply_markup=buttons, reply_to_message_id=message.id)

            # ✅ Delete file after sending
            os.remove(file_path)
        
        msg.delete()  # ✅ Remove "Downloading..." message

    except Exception as e:
        msg.edit_text(f"❌ Error: {str(e)}")
