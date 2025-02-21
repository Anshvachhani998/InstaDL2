from pyrogram import Client, filters
import os
import yt_dlp

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Bot is running successfully!")


app = Client

# Function to download Instagram content (reel, post, or story) using yt-dlp
def download_instagram_content(url):
    ydl_opts = {
        'outtmpl': 'downloaded_content.%(ext)s',  # Output file name pattern
        'quiet': True,  # To suppress logs
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Return the filename of the downloaded file
    return 'downloaded_content.mp4'  # You can modify this based on the content type


@app.on_message(filters.command('dl'))
async def download_content(client, message):
    # Extract the URL from the message
    if len(message.command) < 2:
        await message.reply("⚠️ Please provide an Instagram URL (Reel/Post/Story).")
        return
    
    url = message.command[1]

    try:
        # Download the content
        await message.reply("⬇️ Downloading the content...")
        video_path = download_instagram_content(url)
        
        # Upload the video to Telegram
        await message.reply_video(video_path, caption="Instagram Content")
        
        # Clean up the downloaded file after upload
        os.remove(video_path)
    
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
