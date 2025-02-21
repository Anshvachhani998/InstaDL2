from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instagrapi import Client as InstaClient
import os
import re
import requests
import traceback  
import time  
from urllib.parse import urlparse, parse_qs  
from info import LOG_CHANNEL  

INSTAGRAM_SESSION_FILE = "session.json"

insta_client = InstaClient()
if os.path.exists(INSTAGRAM_SESSION_FILE):
    insta_client.load_settings(INSTAGRAM_SESSION_FILE)
else:
    insta_client.login("harshvi_039", "Ansh123@123")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)

# ✅ Match only Instagram "Post" links
INSTAGRAM_POST_REGEX = r"(https?:\/\/www\.instagram\.com\/p\/[A-Za-z0-9_-]+)"

def download_file(url, user_id, index, is_video):
    """✅ Download media with unique filename"""
    timestamp = int(time.time())  
    ext = "mp4" if is_video else "jpg"
    filename = f"downloads/{user_id}_{timestamp}_{index}.{ext}"  

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
    msg = message.reply_text("📥 **Downloading Post...**")  

    try:
        media_pk = insta_client.media_pk_from_url(url)  
        media_info = insta_client.media_info(media_pk)  

        user_id = message.from_user.id
        first_name = message.from_user.first_name or "Unknown User"

        # ✅ Extract img_index from URL if available
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        img_index = int(query_params.get("img_index", [1])[0]) - 1  # Convert to 0-based index

        media_items = []

        # ✅ Multiple Images/Videos Post
        if hasattr(media_info, "resources") and media_info.resources:
            if 0 <= img_index < len(media_info.resources):
                resource = media_info.resources[img_index]  # ✅ Select only the requested index
                file_path = None
                is_video = False

                if resource.media_type == 2 and hasattr(resource, "video_url"):  # ✅ Video
                    file_path = download_file(resource.video_url, user_id, img_index, is_video=True)
                    is_video = True
                elif resource.media_type == 1 and hasattr(resource, "display_url"):  # ✅ Image
                    file_path = download_file(resource.display_url, user_id, img_index, is_video=False)

                if file_path:
                    media_items.append((file_path, is_video))
            else:
                raise ValueError("⚠ The requested post index is invalid.")

        # ✅ Single Image or Video Post
        else:
            file_path = None
            is_video = False

            if media_info.media_type == 2 and hasattr(media_info, "video_url"):
                file_path = download_file(media_info.video_url, user_id, 0, is_video=True)
                is_video = True
            elif media_info.media_type == 1 and hasattr(media_info, "display_url"):
                file_path = download_file(media_info.display_url, user_id, 0, is_video=False)

            if file_path:
                media_items.append((file_path, is_video))

        if not media_items:
            raise ValueError("⚠ No media found in this post.")  

        caption_user = "🖼 **Here is your post!**\n\n📌 *Provided by* @Ans_Links"
        buttons_user = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Update Channel", url="https://t.me/Ans_Links")]
        ])

        caption_log = f"✅ **Downloaded By:** {first_name} (Telegram ID: `{user_id}`)\n📌 **Source:** [Click Here]({url})"

        # ✅ Send the requested media file
        for file_path, is_video in media_items:
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
