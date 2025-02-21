from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instagrapi import Client as InstaClient
import os
import re
import requests
import traceback  
import time  
import threading  # ✅ Background me download ke liye
from info import LOG_CHANNEL

INSTAGRAM_SESSION_FILE = "session.json"

insta_client = InstaClient()
if os.path.exists(INSTAGRAM_SESSION_FILE):
    insta_client.load_settings(INSTAGRAM_SESSION_FILE)
else:
    insta_client.login("harshvi_039", "Ansh123@123")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)

# ✅ Instagram Reels Regex
INSTAGRAM_REEL_REGEX = r"(https?:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+)"

def download_file(url, user_id):
    """✅ Fast File Download with Timeout & Threads"""
    timestamp = int(time.time())  
    filename = f"downloads/{user_id}_{timestamp}.mp4"  
    os.makedirs("downloads", exist_ok=True)  

    try:
        response = requests.get(url, stream=True, timeout=10)  # ✅ Timeout 10s for faster response
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(4096):  # ✅ Increased chunk size (Fast download)
                    file.write(chunk)

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                return filename  
    except requests.exceptions.Timeout:
        return None  # ✅ Timeout case me None return hoga

    return None  

def send_video(client, chat_id, file_path, caption, buttons, reply_id):
    """✅ Video ko background me bhejne ke liye thread use kar rahe hain"""
    try:
        client.send_video(
            chat_id=chat_id,
            video=file_path,
            caption=caption,
            reply_markup=buttons,
            reply_to_message_id=reply_id
        )
        os.remove(file_path)  # ✅ File Delete after sending
    except Exception as e:
        print(f"Error Sending Video: {e}")

@Client.on_message(filters.regex(INSTAGRAM_REEL_REGEX))  
def download_instagram_reel(client, message):
    url = re.search(INSTAGRAM_REEL_REGEX, message.text).group(0)  
    msg = message.reply_text("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷**")
    
    try:
        start_time = time.time()  # ✅ Execution Time Check
        media_pk = insta_client.media_pk_from_url(url)  
        media_info = insta_client.media_info(media_pk)  

        user_id = message.from_user.id
        first_name = message.from_user.first_name or "Unknown User"

        if not media_info.video_url:
            raise ValueError("⚠ No video found in this reel.")  

        file_path = download_file(media_info.video_url, user_id)

        if file_path:
            caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Rᴇᴇʟꜱ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links**"
            buttons_user = InlineKeyboardMarkup([
                [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/Ans_Links")]
            ])

            caption_log = f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ:** **{message.from_user.mention}**\n📌 **Sᴏᴜʀᴄᴇ URL: [Cʟɪᴄᴋ Hᴇʀᴇ]({url})**"

            # ✅ Threaded video sending (No delay)
            threading.Thread(target=send_video, args=(client, message.chat.id, file_path, caption_user, buttons_user, message.id)).start()
            threading.Thread(target=send_video, args=(client, LOG_CHANNEL, file_path, caption_log, None, None)).start()

        msg.delete()  
        end_time = time.time()
        print(f"✅ Execution Time: {end_time - start_time:.2f}s")  # ✅ Time taken for download

    except ValueError as ve:
        msg.edit_text(str(ve))
    except Exception as e:
        msg.edit_text("⚠ An error occurred while processing your request.")
        error_details = f"❌ **Error Log:**\n\n**User:** {first_name} (`{user_id}`)\n**URL:** {url}\n**Error:** `{str(e)}`\n\n```{traceback.format_exc()}```"
        client.send_message(LOG_CHANNEL, error_details)
