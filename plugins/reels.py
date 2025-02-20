from pyrogram import Client, filters
from instagrapi import Client as InstaClient
import os
import re

# Initialize Instagram Client
INSTAGRAM_SESSION_FILE = "session.json"
insta_client = InstaClient()

# ✅ Instagram link detect karne ke liye regex
INSTAGRAM_LINK_REGEX = r"(https?:\/\/www\.instagram\.com\/(?:p|reel|tv)\/[A-Za-z0-9_-]+)"

@Client.on_message(filters.regex(INSTAGRAM_LINK_REGEX))  # ✅ Jab koi Instagram link send kare
def download_instagram_media(client, message):
    url = re.search(INSTAGRAM_LINK_REGEX, message.text).group(0)  # ✅ Extract Instagram link
    message.reply_text("⏳ Downloading... Please wait!")

    try:
        media_pk = insta_client.media_pk_from_url(url)  # ✅ Get media_pk
        media_info = insta_client.media_info(media_pk)  # ✅ Get media details
        
        if media_info.video_url:
            message.reply_video(media_info.video_url, reply_to_message_id=message.id)  # ✅ Reply me send karega
        elif media_info.thumbnail_url:
            message.reply_photo(media_info.thumbnail_url, reply_to_message_id=message.id)
        else:
            message.reply_text("❌ No media found in this post.", reply_to_message_id=message.id)

    except Exception as e:
        message.reply_text(f"❌ Error: {str(e)}", reply_to_message_id=message.id)
      
