import random
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL, LOG_CHANNEL

app = Client("instagram_bot")

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


INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|tv|p)/[^\s]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    url = message.matches[0].group(0)
    user_id = message.from_user.id

    try:
        downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷**")
        
        video_url = fetch_video_url(url)
        if not video_url:
            await downloading_msg.edit(f"**⚠ No reel found in this url**")
            return
        
        caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Rᴇᴇʟꜱ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Links**"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/Ans_Links")]
        ])

        await message.reply_video(video_url, caption=caption_user, reply_markup=buttons)
        await client.send_video(DUMP_CHANNEL, video=video_url, caption=f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ: {message.from_user.mention}**\n📌 **Sᴏᴜʀᴄᴇ URL: [Click Here]({url})**")
        await downloading_msg.delete()

    except Exception as e:
        error_message = f"🚨 **Error Alert!**\n\n🔹 **User:** {message.from_user.mention}\n🔹 **URL:** {url}\n🔹 **Error:** `{str(e)}`"
        

        await client.send_message(LOG_CHANNEL, error_message)

        
        await message.reply(f"**⚠ Something went wrong. Please contact [ADMIN](https://t.me/AnS_team) for support.**")
