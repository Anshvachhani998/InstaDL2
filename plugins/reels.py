import random
import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL



app = Client

def generate_filename(user_id):
    """Filename user_id + unique 3-digit number + 'Ansh' format me generate karega"""
    unique_number = random.randint(100, 999)  # 3-digit random number
    return f"{user_id}_{unique_number}_Ansh.mp4"

def download_instagram_content(url, filename):
    ydl_opts = {
        'outtmpl': filename,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename

# Instagram Reels/Post/Story Links Detect Karne Ka Regex
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|tv)/[^\s]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    url = message.matches[0].group(0)  # Extract URL from message
    user_id = message.from_user.id  # User ka unique Telegram ID
    filename = generate_filename(user_id)  # Unique filename generate karna

    try:
        # Send downloading message
        downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷**")
        video_path = download_instagram_content(url, filename)

        # Caption for logging
        caption_log = (
            f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ: {message.from_user.mention}**\n"
            f"📌 **Sᴏᴜʀᴄᴇ URL: [Cʟɪᴄᴋ Hᴇʀᴇ]({url}**)"
        )

        caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Rᴇᴇʟꜱ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links**"
             
        # Inline Keyboard Button (Source & Share)
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/Ans_Links")]           
        ])

        # ✅ Send video to user with button
        await message.reply_video(video_path, caption=caption_user, reply_markup=buttons)

        # ✅ Send video to dump channel
        await client.send_video(DUMP_CHANNEL, video=video_path, caption=caption_log)

        # ✅ Delete downloading message
        await downloading_msg.delete()

        os.remove(video_path)  # Cleanup after upload

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
      
