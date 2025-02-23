from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed

API_URL = "https://url-short-web.onrender.com/profile?username={}"

@Client.on_message(filters.command("profile"))
async def profile_cmd(client, message: Message):
    """Handle /profile <username> command with force subscription"""
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id, FORCE_CHANNEL):
        await force_subscribe_message(client, message, user_id)
        return

    if len(message.command) < 2:
        await message.reply("❌ **Usage:** `/profile <username>`")
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

        response = requests.get(API_URL.format(username))
        data = response.json()

        if "error" in data:
            await loading_msg.edit(f"❌ **Error:** {data['error']}")
            return

        full_name = data.get("name", "N/A")
        bio = data.get("bio", "N/A")
        followers = data.get("followers", "N/A")
        following = data.get("following", "N/A")
        profile_pic = data.get("profile_pic", None)

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

        await loading_msg.delete()

    except Exception as e:
        await message.reply(f"❌ **Error fetching profile:** `{str(e)}`")


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
  
