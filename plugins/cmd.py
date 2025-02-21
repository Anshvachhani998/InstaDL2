import os
import logging 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import LOG_CHANNEL
from database.db import db

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/AnS_Bots")]
    ])
    if not await db.is_user_exist(user_id):
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


