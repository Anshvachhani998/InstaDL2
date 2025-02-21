from pyrogram import Client, filters
import os
import yt_dlp

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! Bot is running successfully!")


app = Client




def download_instagram_content(url):
    ydl_opts = {
        'outtmpl': 'downloaded_content.%(ext)s',  # Output filename pattern
        'quiet': True,  # Suppress output for quiet download
        'cookie': {
            'csrftoken': 'T16wSVNGvVabf3CZgXFybsLsrPNPGey6',
            'ds_user_id': '67619570916',
            'sessionid': '67619570916%3AubaN9MmvK9BL88%3A12%3AAYfGTq96_M345-XC9ugTSiUWJspUQq7adusRxccpFw',
            'mid': 'Z7hvngABAAHbVf-Otq4JVgnFw_ow',
            'ig_did': '1CDEC179-E824-4C8A-BF41-83CED145CF4F',
            'ig_nrcb': '1',
            'dpr': '3',
            'datr': 'nW-4Z2_2v596GZiBAvFvI5qX',
            'wd': '360x692',
            'rur': '"LDC\\05467619570916\\0541771676712:01f7df0ea4d064491987c35e8417ce9e7695421b72f1990b1b62ff694777199ee316d0fc"',
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return 'downloaded_content.mp4'




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
