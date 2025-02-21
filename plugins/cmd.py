from pyrogram import Client, filters
import os
import yt_dlp
import subprocess

# Bot Start Command
@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Bot is running successfully!")

app = Client

def generate_filename(user_id):
    """Filename user_id + 'Ansh' format me generate karega"""
    return f"{user_id}_Ansh.mp4"

def fix_metadata(video_path):
    """ffmpeg se metadata fix karega taaki duration Telegram pe sahi dikhe"""
    fixed_path = f"fixed_{video_path}"
    command = f'ffmpeg -i "{video_path}" -c copy -map 0 -movflags +faststart "{fixed_path}"'
    subprocess.run(command, shell=True)
    return fixed_path

def download_instagram_content(url, filename):
    """Instagram Video Highest Quality me Download karega"""
    ydl_opts = {
        'outtmpl': filename,
        'quiet': True,
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best',  # Highest Quality Format
        'postprocessors': [{'key': 'FFmpegMetadata'}]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename

# Instagram Reels/Post/Story/TV Links Detect Karne Ka Regex
INSTAGRAM_REGEX = r"(https?://www\.instagram\.com/(reel|p|stories|tv)/[^\s]+)"

@app.on_message(filters.regex(INSTAGRAM_REGEX))
async def download_content(client, message):
    url = message.matches[0].group(0)  # Extract URL from message
    user_id = message.from_user.id  # User ka unique Telegram ID
    filename = generate_filename(user_id)  # Unique filename generate karna

    try:
        await message.reply("⬇️ Downloading the Instagram content in best quality...")
        video_path = download_instagram_content(url, filename)

        # Metadata Fix using ffmpeg
        fixed_video_path = fix_metadata(video_path)

        # Upload video to Telegram
        await message.reply_video(fixed_video_path, caption="Instagram Content (Best Quality)")

        # Cleanup after upload
        os.remove(video_path)
        os.remove(fixed_video_path)

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
