from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

API_URL = "https://url-short-web.onrender.com/profile?username={}"

def fetch_profile(username):
    """API se Instagram profile details fetch karega"""
    try:
        response = requests.get(API_URL.format(username))
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:      
        return None
        
@Client.on_message(filters.command("profile"))
async def profile_cmd(client, message: Message):
    """Handle /profile <username> command with force subscription"""
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        await force_subscribe_message(client, message, user_id)
        return

    # ⚠ Fix: Agar koi username provide nahi kiya toh proper reply bheje
    if len(message.command) < 2:
        await message.reply("⚡ **Incorrect Usage!**\n\n"
                           "🔹 To fetch an Instagram profile, use:\n`/profile <username>`\n"
                           "🔹 Or just send an Instagram profile link.")
        return

    username = message.command[1]
    await fetch_instagram_profile(client, message, username)


@Client.on_message(filters.regex(r"https?://(www\.)?instagram\.com/([A-Za-z0-9_.]+)"))
async def profile_link_handler(client, message: Message):
    """Handle Instagram profile link messages with force subscription"""
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        await force_subscribe_message(client, message, user_id)
        return

    username = message.matches[0].group(2)  # Extract username from the link
    await fetch_instagram_profile(client, message, username)


async def fetch_instagram_profile(client, message, username):
    """Fetch Instagram profile details using API"""
    try:
        loading_msg = await message.reply("**🔍 ꜰᴇᴛᴄʜɪɴɢ ɪɴꜱᴛᴀɢʀᴀᴍ ᴘʀᴏꜰɪʟᴇ 🩷**")

        
        profile = fetch_profile(username)
        if not profile:
            await loading_msg.edit(f"⚠️ ᴜꜱᴇʀɴᴀᴍᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ!")
            return

        full_name = profile.get("name", "N/A")
        bio = profile.get("bio", "N/A")
        followers = profile.get("followers", "N/A")
        following = profile.get("following", "N/A")
        profile_pic = profile.get("profile_pic", None)

        caption = (
            f"👤 **Instagram Profile:** [{username}](https://instagram.com/{username})\n\n"
            f"📌 **Name:** {full_name}\n"
            f"📖 **Bio:** {bio}\n"
            f"👥 **Followers:** {followers}\n"
            f"✅ **Following:** {following}\n\n"
            "**🔹 Powered by @Ans_Bots**"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 View Profile", url=f"https://instagram.com/{username}")],
            [InlineKeyboardButton("🌟 Update Channel", url="https://t.me/AnS_Bots")]
        ])

        if profile_pic:
            await message.reply_photo(photo=profile_pic, caption=caption, reply_markup=buttons)
        else:
            await message.reply_text(caption, reply_markup=buttons)

        
        user_mention = message.from_user.mention
        dump_caption = f"**✅ ᴘʀᴏꜰɪʟᴇ ꜱᴇᴀʀᴄʜᴇᴅ ʙʏ:** {user_mention}\n**📌ᴘʀᴏꜰɪʟᴇ ᴜʀʟ:** [{username}](https://instagram.com/{username})"

        await client.send_message(DUMP_CHANNEL, dump_caption)
        
        await loading_msg.delete()

    except Exception as e:
        error_message = f"🚨 **Error Alert!**\n\n🔹 **User:** {mention or message.from_user.mention}\n🔹 **URL:** {url}\n🔹 **Error:** `{str(e)}`"
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
