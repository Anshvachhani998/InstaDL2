from pyrogram import Client, filters
import os
import yt_dlp

# Bot Start Command
@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Bot is running successfully!")

app = Client

def download_instagram_content(url):
    ydl_opts = {
        'outtmpl': 'downloaded_content.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return 'downloaded_content.mp4'

# Instagram Reels/Post/Story Links Detect Karne Ka Regex
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|tv)/[^\s]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    url = message.matches[0].group(0)  # Extract URL from message

    try:
        await message.reply("⬇️ Downloading the Instagram content...")
        video_path = download_instagram_content(url)
        
        await message.reply_video(video_path, caption="Instagram Content")
        
        os.remove(video_path)  # Cleanup after upload
    
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
