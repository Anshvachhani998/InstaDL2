import random
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed  # ✅ Import from utils

app = Client

API_ENDPOINT = "https://instaapi-green.vercel.app/convert?url={}"

def fetch_video_url(instagram_url):
    """API endpoint se direct video URL fetch karega"""
    try:
        response = requests.get(API_ENDPOINT.format(instagram_url))
        data = response.json()
        return data.get("dwn_url")
    except Exception:
        return None

INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|tv|p)/[^\s?]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    user_id = message.from_user.id
    url = message.matches[0].group(0)

    # ✅ **Force Subscription Check**
    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        invite_link = await get_invite_link(client, FORCE_CHANNEL)
        if not invite_link:
            return await message.reply("🚨 **Error generating invite link! Contact admin.**")

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ 🔥", url=invite_link)],
            [InlineKeyboardButton("🔓 I'ᴠᴇ Jᴏɪɴᴇᴅ, Rᴇᴛʀʏ ✅", callback_data="check_sub")]
        ])
        return await message.reply(
            "**🔒 Aᴄᴄᴇss Dᴇɴɪᴇᴅ!**\n\n"
            "🔹 Tᴏ ᴜsᴇ ᴛʜɪs Bᴏᴛ, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴏғғɪᴄɪᴀʟ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.\n"
            "🔹 Aғᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴘʀᴇss **'🔄 I'ᴠᴇ Jᴏɪɴᴇᴅ'** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\n\n",         
            reply_markup=buttons
        )

    try:
        downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Rᴇᴇʟꜱ 🩷**")
        
        video_url = fetch_video_url(url)
        if not video_url:
            await downloading_msg.edit(f"**⚠ No reel found in this URL**")
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

@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id
    message = callback_query.message
    original_message = message.reply_to_message  # Original message containing the Instagram URL

    if await is_subscribed(client, user_id, FORCE_CHANNEL):
        await message.edit_text("✅ **Thank you for joining! Downloading your reel now...**")

        # After joining, check if the user sent an Instagram link
        async for last_message in client.get_chat_history(user_id, limit=1):
            last_message_text = last_message.text
            if last_message_text and re.match(INSTAGRAM_REGEX, last_message_text):  # Check if it's an Instagram URL
                await download_content(client, last_message)  # Run the download process for this URL
            else:
                await callback_query.answer("⚠ No Instagram URL found in your last message.", show_alert=True)
    else:
        await callback_query.answer("🚨 You are not subscribed yet!", show_alert=True)
