import random
import aiohttp  # Use aiohttp for async HTTP requests
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from info import DUMP_CHANNEL, LOG_CHANNEL, FORCE_CHANNEL
from utils import get_invite_link, is_subscribed
from database.db import db
import logging 
from asyncio import create_task

logger = logging.getLogger(__name__)

app = Client

ADVANCE_API = "https://instadl-api.koyeb.app/post?url={}"
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(p)/[^\s?]+)"


async def advance_fatch_url(instagram_url):
    """API endpoint se direct media URL fetch karega"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ADVANCE_API.format(instagram_url)) as response:
                data = await response.json()        
                media_urls = data.get("media", [])        
                return media_urls if media_urls else None  # Jo bhi list mile, wo return hoga
    except Exception:
        return None



async def advance_content(client, message, url, user_id, mention=None):
    """Function to download the Instagram content"""
    try:
        downloading_msg = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ Pᴏꜱᴛ 🩷**")
        
        media_urls = await advance_fatch_url(url)  # API se media URLs fetch karna
        
        if not media_urls:
            await downloading_msg.edit(
                "** Unable to retrieve publication information.**\n\n"
                "This could be due to the following reasons:\n"
                "▫️ The account is private or closed.\n"
                "▫️ A data retrieval error occurred.\n"
                "▫️ The content might be restricted due to age or copyright limitations.\n\n"
                "⚠ **If the issue persists, please inform the admin or ask for help in our support group.**\n\n"
                "**💬 Support Group: [SUPPORT](https://t.me/AnSBotsSupports)**",
                disable_web_page_preview=True
            )
            error_message =f"**Error**\n **{url}**\n⚠️ Pᴏꜱᴛ Nᴏᴛ Fᴏᴜɴᴅ"
            await client.send_message(LOG_CHANNEL, error_message)       
            return
        
        caption_user = "**ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ Pᴏꜱᴛ 🎥**\n\n**ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ @Ans_Bots**"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 💫", url="https://t.me/AnS_Bots")]
        ])
        
        # Agar ek hi post hai toh sirf ek bhejo
        if len(media_urls) == 1:
            media_url = media_urls[0]
            if ".mp4" in media_url:
                await message.reply_video(media_url, caption=caption_user, reply_markup=buttons)
            else:
                await message.reply_photo(media_url, caption=caption_user, reply_markup=buttons)
        else:
            # Agar multiple media hain toh pehle media ke saath caption bhejo
            batch_size = 10
            for batch_start in range(0, len(media_urls), batch_size):
                album = []
                for i, media_url in enumerate(media_urls[batch_start:batch_start + batch_size]):
                    if ".mp4" in media_url:
                        media = InputMediaVideo(media_url, caption=caption_user if i == 0 and batch_start == 0 else "")
                    else:
                        media = InputMediaPhoto(media_url, caption=caption_user if i == 0 and batch_start == 0 else "")
                    album.append(media)
                
                await message.reply_media_group(album)
            
        await db.increment_download_count()
        await downloading_msg.delete()

    except Exception as e:
        error_message = f"🚨 **Error Alert!**\n\n🔹 **User:** {mention or message.from_user.mention}\n🔹 **URL:** {url}\n🔹 **Error:** `{str(e)}`"
        await client.send_message(LOG_CHANNEL, error_message)
        await message.reply("⚠ Something went wrong. Please contact [ADMIN](https://t.me/AnS_team) for support.")


@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def handle_instagram_link(client, message):
    user_id = message.from_user.id
    url = message.matches[0].group(0)

    # If the user is subscribed, proceed to download directly
    # We make sure the download process runs in the background so it doesn't block.
    create_task(advance_content(client, message, url, user_id))


@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id  # Correct user ID
    mention = callback_query.from_user.mention  # Correct user mention
    url = callback_query.data.split("#")[2]  # Extract URL from callback data
    
    if await is_subscribed(client, user_id, FORCE_CHANNEL):
        an = await callback_query.message.edit_text("**🙏 Tʜᴀɴᴋs Fᴏʀ Jᴏɪɴɪɴɢ! Nᴏᴡ Pʀᴏᴄᴇssɪɴɢ Yᴏᴜʀ Lɪɴᴋ...**")

        # Pass `mention` as a new parameter
        await advance_content(client, callback_query.message, url, user_id, mention)
        await an.delete()
    else:
        await callback_query.answer("🚨 You are not subscribed yet!", show_alert=True)
        
