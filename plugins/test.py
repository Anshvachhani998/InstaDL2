import asyncio
import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip
import instaloader
from pyrogram import types

# Configuration settings
INST_LOGIN = "loveis8507"
INST_PASS = "Ansh12345@23"
OUTPUT_DIR = "downloads"
admin_id = 5961011848  # Replace with your admin user ID

# Instaloader instance
L = instaloader.Instaloader()

bot = Client 

# Asynchronous wait for 2FA code
async def wait_for_code(admin_id):
    code_future = asyncio.Future()
    await bot.send_message(chat_id=admin_id, text="Enter Instagram 2FA code by command /ig_code code")

    @bot.on_message(filters.text.startswith("/ig_code "))
    async def handle_message(message: Message):
        if message.from_user.id == admin_id:
            code_future.set_result(message.text.split(" ", 1)[1])

    return await code_future

# Instagram login with 2FA
async def instaloader_login(L, login, password, admin_id):
    try:
        await asyncio.to_thread(L.load_session_from_file, login)
        print("Login with Session")
    except Exception as e:
        print(e)
        try:
            await asyncio.to_thread(L.close)
            await asyncio.to_thread(L.login, login, password)
            await asyncio.to_thread(L.save_session_to_file)
            print("Login Successful")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            code = str(await wait_for_code(admin_id))
            await asyncio.to_thread(L.two_factor_login, code)
            await asyncio.to_thread(L.save_session_to_file)

# Download command
@bot.on_message(filters.command('download') & filters.text)
async def download_instagram_content(message: Message):
    url = message.text.split(' ', 1)[1]

    if not url:
        await message.reply("Please provide a valid Instagram URL. Example: `/download https://www.instagram.com/p/xyz`")
        return

    # Start login to Instagram
    await instaloader_login(L, INST_LOGIN, INST_PASS, admin_id)
    
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        download_dir = f"{OUTPUT_DIR}.{post.shortcode}"
        post_caption = post.caption

        # Normal caption for the post
        caption_text = f"Here is your Instagram post: {post_caption}"

        L.download_post(post, target=download_dir)

        if "/reel/" in url:
            file_type = "video"

            for root, _, files in os.walk(download_dir):
                for file in files:
                    if file.endswith('.mp4'):
                        file_path = os.path.join(root, file)

                        video_clip = VideoFileClip(file_path)
                        width, height = video_clip.size

                        sent_message = await message.reply_video(video=types.InputFile(file_path),
                                                                  caption=caption_text,
                                                                  width=width, height=height)

                        file_id = sent_message.video.file_id

        else:
            # Send all media if the URL is not for a reel
            media_group = []
            batch_size = 10
            batch = 0
            for root, _, files in os.walk(download_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        media_group.append(types.InputFile(file_path))
                        batch += 1
                    elif file.endswith('.mp4'):
                        media_group.append(types.InputFile(file_path))
                        batch += 1

                    if batch == batch_size:
                        await message.reply_media_group(media=media_group)
                        media_group = []
                        batch = 0

            if batch > 0:
                await message.reply_media_group(media=media_group)

        await asyncio.sleep(5)

        # Clean up downloaded files and directory
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            os.rmdir(download_dir)

    except Exception as e:
        print(e)
        await message.reply("Something went wrong :(\nPlease try again later.")

