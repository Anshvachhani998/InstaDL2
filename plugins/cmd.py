import os
import logging 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import LOG_CHANNEL, ADMINS
from database.db import db

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/AnS_Bots")]
    ])
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL, 
            f"**#NewUser 🔻**\n**ID -> `{message.from_user.id}`**\n**Name -> {message.from_user.mention}**"
        )
    await message.reply_text(
        "💖✨ **Welcome to the Ultimate Instagram Downloader!** ✨💖\n\n"
        "🚀 **Fastest Instagram Reels, Posts & IGTV Video Downloader!** 🎥\n"
        "💫 Just send any Instagram link & get **high-speed downloads instantly!**\n\n"
        "⚡ **Blazing Fast Downloads**\n"
        "✅ **No Watermark, Full HD Quality**\n"
        "🔹 **Unlimited & Secure**\n\n"
        "💖 Enjoy Hassle-Free Downloads! 💖",
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex("start"))
async def start_hendler(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/AnS_Bots")]
    ])
    
    await callback_query.message.edit_text(
        "💖✨ **Welcome to the Ultimate Instagram Downloader!** ✨💖\n\n"
        "🚀 **Fastest Instagram Reels, Posts & IGTV Video Downloader!** 🎥\n"
        "💫 Just send any Instagram link & get **high-speed downloads instantly!**\n\n"
        "⚡ **Blazing Fast Downloads**\n"
        "✅ **No Watermark, Full HD Quality**\n"
        "🔹 **Unlimited & Secure**\n\n"
        "💖 Enjoy Hassle-Free Downloads! 💖",
        reply_markup=buttons
    )
    
@Client.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="start"), InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])
    
    await callback_query.message.edit_text(
        "**❓ Help Guide**\n\n"
        "📌 Just send any Instagram Reel, Post, or IGTV link here.\n"
        "🔹 The bot will instantly download & send it to you in **HD quality**.\n"
        "🚀 **Super Fast & Secure!**\n\n"
        "🎥 **For manual download, use** `/dl <link>` **command.**\n\n" 
        "💖 **Enjoy hassle-free downloads!**",
        reply_markup=buttons
    )

@Client.on_callback_query(filters.regex("about"))
async def about(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="start"), InlineKeyboardButton("❓ Help", callback_data="help")]
    ])
    
    await callback_query.message.edit_text(
        "**ℹ️ About This Bot**\n\n"
        "💎 **Developed By:** [AnS </> Team](https://t.me/AnS_team)\n"
        "🚀 **Purpose:** High-speed Instagram video downloads\n"
        "🎥 **Supports:** Reels, Posts, IGTV\n"
        "🔹 **No watermark, HD quality**\n\n"
        "**💖 Enjoy & Share!**",
        reply_markup=buttons
    )



@Client.on_message(filters.command('users') & filters.private)
async def total_users(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("🚫 **You are not authorized to use this command!**")

    response = await message.reply("🔍 Fetching total users...")

    total_users = await db.total_users_count()

    await response.edit_text(
        f"👑 **Admin Panel**\n\n"
        f"🌍 **Total Users in Database:** `{total_users}`\n\n"
        "🚀 *Thanks for managing this bot!*"
    )
    



import yt_dlp


app = Client

# Function to download Instagram reel using yt-dlp
def download_instagram_reel(url):
    ydl_opts = {
        'outtmpl': 'reel_video.%(ext)s',  # Output file name pattern
        'quiet': True,  # To suppress logs
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Return the filename of the downloaded file
    return 'reel_video.mp4'

@app.on_message(filters.command('dl'))
async def download_reel(client, message):
    # Extract the URL from the message
    if len(message.command) < 2:
        await message.reply("⚠️ Please provide an Instagram reel URL.")
        return
    
    reel_url = message.command[1]

    try:
        # Download the reel
        await message.reply("⬇️ Downloading the reel...")
        video_path = download_instagram_reel(reel_url)
        
        # Upload the video to Telegram
        await message.reply_video(video_path, caption="Instagram Reel")
        
        # Clean up the downloaded file after upload
        os.remove(video_path)
    
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


    
