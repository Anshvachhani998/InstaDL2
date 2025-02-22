import os
import logging 
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import LOG_CHANNEL, ADMINS
from database.db import db
from pyrogram.enums import ParseMode 

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
        "💎 **Developed By: [AnS </> Team](https://t.me/AnS_team)**\n"
        "🚀 **Purpose:** High-speed Instagram video downloads\n"
        "🎥 **Supports:** Reels, Posts, IGTV\n"
        "🔹 **No watermark, HD quality**\n\n"
        "**💖 Enjoy & Share!**",
        reply_markup=buttons,
        parse_mode="Markdown"
    )

@Client.on_message(filters.command("about"))
async def aboutcmd(client, message):
    
    await message.reply(
        "**ℹ️ About This Bot**\n\n"
        "💎 **Developed By: [AnS </> Team](https://t.me/AnS_team)**\n"
        "🚀 **Purpose:** High-speed Instagram video downloads\n"
        "🎥 **Supports:** Reels, Posts, IGTV\n"
        "🔹 **No watermark, HD quality**\n\n"
        "**💖 Enjoy & Share!**",
        parse_mode=enums.ParseMode.Markdown
    )

@Client.on_message(filters.command("help"))
async def helpcmd(client, message):
    
    await message.reply(
        "**❓ Help Guide**\n\n"
        "📌 Just send any Instagram Reel, Post, or IGTV link here.\n"
        "🔹 The bot will instantly download & send it to you in **HD quality**.\n"
        "🚀 **Super Fast & Secure!**\n\n"
        "🎥 **For manual download, use** `/dl <link>` **command.**\n\n" 
        "💖 **Enjoy hassle-free downloads!**"        
    )

@Client.on_message(filters.command("dl"))
async def dlcmd(client, message):
    
    await message.reply(
        "**📌 Just send any Instagram Reel, Post, or IGTV link here.**"        
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
    


@Client.on_message(filters.command("stats") & filters.private)
async def stats(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("🚫 **You are not authorized to use this command!**")
  
    response = await message.reply("**🔍 Fetching Bot Statistics**")

    total_users = await db.total_users_count()
    total_downloads = await db.get_total_downloads()
    
    await response.edit_text(
        f"📊 **Bot Statistics**\n\n"
        f"👥 **Total Users:** {total_users}\n"
        f"⬇️ **Total Downloads:** {total_downloads}\n\n"
        "These stats show the total number of users and downloads recorded in the system."
    )

