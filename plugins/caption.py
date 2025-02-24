from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

API_URL = "https://url-short-web.onrender.com/caption?url={}"

def fetch_caption(instagram_url):
    """API endpoint se direct video URL fetch karega (Only MP4)"""
    try:
        response = requests.get(API_URL.format(instagram_url))
        data = response.json()       
        return data.get("caption")
    except Exception:
        return None
        
@Client.on_message(filters.command("caption"))
async def caption_cmd(client, message: Message):
    """Handle /caption <reel url> command with force subscription"""
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        await force_subscribe_message(client, message, user_id)
        return

    if len(message.command) < 2:
        await message.reply("⚡ **Incorrect Usage!**\n\n"
                            "🔹 Use: `/caption <reel-url>`\n"
                            "🔹 Example: `/caption https://www.instagram.com/reel/xyz123/`")
        return

    url = message.command[1]
    await fetch_instagram_caption(client, message, url)

  

async def fetch_instagram_caption(client, message, url):
    """Fetch Instagram profile details using API"""
    try:
        loading_msg = await message.reply("**🔍 Fᴇᴛᴄʜɪɴɢ Rᴇᴇʟs Cᴀᴘᴛɪᴏɴ...🩷**")

        caption = fetch_caption(url)

        if not caption:
            await loading_msg.edit("⚠️ Cᴀᴘᴛɪᴏɴ Nᴏᴛ Fᴏᴜɴᴅ!")
            return

        
        buttons = InlineKeyboardMarkup([        
            [InlineKeyboardButton("🌟 Update Channel", url="https://t.me/AnS_Bots")]
        ])

        
        await message.reply_text(caption, reply_markup=buttons)

        
        user_mention = message.from_user.mention
        dump_caption = f"**✅ Cᴀᴘᴛɪᴏɴ ꜱᴇᴀʀᴄʜᴇᴅ ʙʏ:** {user_mention}\n**📌 ᴜʀʟ:** [URL](https://instagram.com/{url})"

        await client.send_message(DUMP_CHANNEL, dump_caption, disable_web_page_preview=True)
        
        await loading_msg.delete()

    except Exception as e:
        error_message = f"🚨 **Error Alert!**\n\n🔹 **User:** {message.from_user.mention}\n🔹 **URL:** {url}\n🔹 **Error:** `{str(e)}`"
        await client.send_message(LOG_CHANNEL, error_message)
        await message.reply(f"**⚠ Something went wrong. Please contact [ADMIN](https://t.me/AnS_team) for support.**")


async def force_subscribe_message(client, message, user_id):
    """Send force subscribe message if user is not in the channel"""
    invite_link = await get_invite_link(client, FORCE_CHANNEL)
    if not invite_link:
        return await message.reply("🚨 **Error generating invite link! Contact admin.**")

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ 🔥", url=invite_link)],
        [InlineKeyboardButton("🔓 I'ᴠᴇ Jᴏɪɴᴇᴅ, Rᴇᴛʀʏ ✅", callback_data=f"check_sub#{user_id}")]
    ])

    await message.reply(
        "**🔒 Aᴄᴄᴇss Dᴇɴɪᴇᴅ!**\n\n"
        "🔹 Tᴏ ᴜsᴇ ᴛʜɪs Bᴏᴛ, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴏғғɪᴄɪᴀʟ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.\n"
        "🔹 Aғᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴘʀᴇss **'🔄 I'ᴠᴇ Jᴏɪɴᴇᴅ'** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\n\n",
        reply_markup=buttons
    )
  



@Client.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id  # Correct user ID
    mention = callback_query.from_user.mention  # Correct user mention
    
    if await is_subscribed(client, user_id, FORCE_CHANNEL):
        an = await callback_query.message.edit_text("**🙏 Tʜᴀɴᴋs Fᴏʀ Jᴏɪɴɪɴɢ! 🔓 Aᴄᴄᴇss Bᴏᴛ**")
        
    else:
        await callback_query.answer("🚨 You are not subscribed yet!", show_alert=True)

