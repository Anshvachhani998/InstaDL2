import random
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL

app = Client

API_ENDPOINT = "https://instaapi-green.vercel.app/convert?url={}"

def generate_filename(user_id):
    """Unique filename generate karega"""
    unique_number = random.randint(100, 999)
    return f"{user_id}_{unique_number}_Ansh.mp4"

def fetch_video_url(instagram_url):
    """API endpoint se direct video URL fetch karega"""
    try:
        response = requests.get(API_ENDPOINT.format(instagram_url))
        data = response.json()
        return data.get("dwn_url")
    except Exception:
        return None

# Instagram Reels/Post/Story Links Detect Karne Ka Regex
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|tv)/[^\s]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    url = message.matches[0].group(0)
    user_id = message.from_user.id

    try:
        downloading_msg = await message.reply("**Fᴇᴛᴄʜɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ... 🎥**")
        
        video_url = fetch_video_url(url)
        if not video_url:
            await downloading_msg.edit("❌ Failed to fetch video link.")
            return
        
        caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Rᴇᴇʟꜱ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links**"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/Ans_Links")]
        ])

        await message.reply_video(video_url, caption=caption_user, reply_markup=buttons)
        await client.send_video(DUMP_CHANNEL, video=video_url, caption=f"✅ **Downloaded by {message.from_user.mention}**\n📌 **Source URL: [Click Here]({url})**")
        await downloading_msg.delete()

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
