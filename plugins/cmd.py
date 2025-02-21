from pyrogram import Client, filters
import os
import yt_dlp

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Bot is running successfully!")


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


    
