import random
import requests
import re
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed
from database.db import db

app = Client

ADVANCE_API = "https://url-short-web.onrender.com/story?url={}"
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(stories)/[^\s?]+)"



def advance_fatch_url(instagram_url):
    """API endpoint se direct video URL fetch karega"""
    try:
        response = requests.get(ADVANCE_API.format(instagram_url))
        data = response.json()
        return data.get("story_url")
    except Exception:
        return None
        
async def download_content(client, message, url, user_id, mention=None):
    """Function to download the Instagram content"""
    try:
        downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Sᴛᴏʀʏ ɪɴ 5 ꜱᴇᴄᴏɴᴅꜱ🩷**")
        
        video_url = advance_fatch_url(url)
        if not video_url:
            await downloading_msg.edit(
                "** Unable to retrieve publication information.**\n\n"
                "This could be due to the following reasons:\n"
                "▫️ The account is private or closed.\n"
                "▫️ A data retrieval error occurred.\n"
                "▫️ The content might be restricted due to age or copyright limitations.\n\n"
                "**Please inform the admin if the issue persists. You can contact the admin directly here: [ADMIN](https://t.me/AnS_team).**",
                disable_web_page_preview=True
            )
            return
        
        caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ꜱᴛᴏʀʏ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Bots**"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/AnS_Bots")]
        ])

        await message.reply_video(video_url, caption=caption_user, reply_markup=buttons)

        # `mention` ko check karenge, agar None hai toh `message.from_user.mention` use karenge
        user_mention = mention or message.from_user.mention  

        await client.send_video(DUMP_CHANNEL, video=video_url, caption=f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ: {user_mention}**\n📌 **Sᴏᴜʀᴄᴇ URL: [Click Here]({url})**")
        await db.increment_download_count()
        await downloading_msg.delete()

    except Exception as e:
        error_message = f"🚨 **Error Alert!**\n\n🔹 **User:** {mention or message.from_user.mention}\n🔹 **URL:** {url}\n🔹 **Error:** `{str(e)}`"
        await client.send_message(LOG_CHANNEL, error_message)
        await message.reply(f"**⚠ Something went wrong. Please contact [ADMIN](https://t.me/AnS_team) for support.**")


@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def handle_instagram_link(client, message):
    user_id = message.from_user.id
    url = message.matches[0].group(0)

    # ✅ **Force Subscription Check**
    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        invite_link = await get_invite_link(client, FORCE_CHANNEL)
        if not invite_link:
            return await message.reply("🚨 **Error generating invite link! Contact admin.**")

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ 🔥", url=invite_link)],
            [InlineKeyboardButton("🔓 I'ᴠᴇ Jᴏɪɴᴇᴅ, Rᴇᴛʀʏ ✅", callback_data=f"check_sub#{user_id}#{url}")]
        ])
        return await message.reply(
            "**🔒 Aᴄᴄᴇss Dᴇɴɪᴇᴅ!**\n\n"
            "🔹 Tᴏ ᴜsᴇ ᴛʜɪs Bᴏᴛ, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴏғғɪᴄɪᴀʟ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.\n"
            "🔹 Aғᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴘʀᴇss **'🔄 I'ᴠᴇ Jᴏɪɴᴇᴅ'** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\n\n",         
            reply_markup=buttons
        )

    # If the user is subscribed, proceed to download directly
    await download_content(client, message, url, user_id)

@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id  # Correct user ID
    mention = callback_query.from_user.mention  # Correct user mention
    url = callback_query.data.split("#")[2]  # Extract URL from callback data
    
    if await is_subscribed(client, user_id, FORCE_CHANNEL):
        an = await callback_query.message.edit_text("**🙏 Tʜᴀɴᴋs Fᴏʀ Jᴏɪɴɪɴɢ! Nᴏᴡ Pʀᴏᴄᴇssɪɴɢ Yᴏᴜʀ Lɪɴᴋ...**")

        # Pass `mention` as a new parameter
        await download_content(client, callback_query.message, url, user_id, mention)
        await an.delete()
    else:
        await callback_query.answer("🚨 You are not subscribed yet!", show_alert=True)
