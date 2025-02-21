from pyrogram import Client, filters
import os
import yt_dlp

# Bot Start Command
@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Bot is running successfully!")

app = Client

def generate_filename(user_id):
    """Filename user_id + 'Ansh' format me generate karega"""
    return f"{user_id}_Ansh.mp4"

def download_instagram_content(url, filename):
    ydl_opts = {
        'outtmpl': filename,
        'quiet': True,
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]',  # Best video + best audio
        'merge_output_format': 'mp4',  # Merge into MP4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename

# Instagram Reels/Post/Story Links Detect Karne Ka Regex
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|tv|stories)/[^\s]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    url = message.matches[0].group(0)  # Extract URL from message
    user_id = message.from_user.id  # User ka unique Telegram ID
    filename = generate_filename(user_id)  # Unique filename generate karna

    try:
        await message.reply("⬇️ Downloading the Instagram content in high quality...")
        video_path = download_instagram_content(url, filename)
        
        await message.reply_video(video_path, caption="📥 Downloaded in Best Quality")
        
        os.remove(video_path)  # Cleanup after upload
    
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
