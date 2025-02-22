import instaloader
import os
import shutil
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client # ✅ Client object properly initialize karo

# ✅ Instagram Username
USERNAME = "loveis8507"
SESSION_FILE = f"session-{USERNAME}"

otp_required = False  # OTP Flag
PASSWORD = None  # Store Password Temporarily

# ✅ /login <password> - Instagram Login Command
@app.on_message(filters.command("login"))
async def login_instagram(client, message: Message):
    global otp_required, PASSWORD
    
    L = instaloader.Instaloader()

    if os.path.exists(SESSION_FILE):
        L.load_session_from_file(USERNAME)
        await message.reply_text("✅ Logged in using saved session!")
        return
    
    if len(message.command) < 2:
        await message.reply_text("❌ Usage: `/login <password>`")
        return

    PASSWORD = message.command[1]

    try:
        L.login(USERNAME, PASSWORD)
        L.save_session_to_file(SESSION_FILE)  # ✅ Session manually save karo
        await message.reply_text("✅ Login successful & session saved!")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        otp_required = True
        await message.reply_text("🔢 Enter OTP using `/otp <code>`")
    except Exception as e:
        await message.reply_text(f"❌ Login failed: {e}")

# ✅ /otp - Handle OTP Input
@app.on_message(filters.command("otp"))
async def handle_otp(client, message: Message):
    global otp_required
    
    if not otp_required:
        await message.reply_text("❌ OTP is not required. Use `/login` first.")
        return
    
    if len(message.command) < 2:
        await message.reply_text("Usage: `/otp <code>`")
        return

    otp_code = message.command[1]
    
    L = instaloader.Instaloader()
    
    try:
        L.two_factor_login(otp_code)
        L.save_session_to_file(SESSION_FILE)
        otp_required = False
        await message.reply_text("✅ OTP verified & login successful!")
    except Exception as e:
        await message.reply_text(f"❌ OTP verification failed: {e}")

# ✅ /session - Check if Session Exists
@app.on_message(filters.command("session"))
async def check_session(client, message: Message):
    if os.path.exists(SESSION_FILE):
        await message.reply_text(f"✅ Logged in with a saved session: `{SESSION_FILE}`")
    else:
        await message.reply_text("❌ No session found. Please use `/login` first.")

# ✅ /clear_session - Delete Session File
@app.on_message(filters.command("clear_session"))
async def clear_session(client, message: Message):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        await message.reply_text("🗑️ Session cleared! Use `/login` to login again.")
    else:
        await message.reply_text("❌ No session file found.")

# ✅ /dl <instagram_url> - Download Instagram Reel/Post
@app.on_message(filters.command("dl"))
async def download_instagram(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Usage: `/dl <instagram_url>`")
        return

    url = message.command[1]
    shortcode = url.split("/")[-2]  # ✅ Extract Instagram Post ID

    await message.reply_text("🔄 Downloading... Please wait!")

    # ✅ Instaloader Instance
    L = instaloader.Instaloader()

    # ✅ Session Load Karo Agar File Hai
    if os.path.exists(SESSION_FILE):
        L.load_session_from_file(USERNAME)

    # ✅ Create "downloads" Folder
    download_path = "downloads"
    os.makedirs(download_path, exist_ok=True)

    try:
        # ✅ Download Post/Reel
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=download_path)

        # ✅ Find the downloaded video file
        video_file = None
        for file in os.listdir(download_path):
            if file.endswith(".mp4"):
                video_file = os.path.join(download_path, file)
                break

        if video_file:
            # ✅ Upload to Telegram
            await message.reply_video(video_file, caption="✅ Reel downloaded successfully!")

            # ✅ Clean up the folder
            shutil.rmtree(download_path)
        else:
            await message.reply_text("❌ Download failed. No video found!")

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")



# ✅ /session_export - Export Session Data
@app.on_message(filters.command("session_export"))
async def export_session(client, message: Message):
    if not os.path.exists(SESSION_FILE):
        await message.reply_text("❌ No session file found. Please use `/login` first.")
        return

    # ✅ Read session file
    with open(SESSION_FILE, "rb") as f:
        session_data = f.read()


    await message.reply_text(f"```{session_data}```", quote=True)


@app.on_message(filters.command("session_import"))
async def import_session(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Usage: `/session_import <session_data>`")
        return

    session_data = message.text.split(maxsplit=1)[1]  # Extract session data from message

    # ✅ Save session data to file
    with open(SESSION_FILE, "w") as f:
        f.write(session_data)

    await message.reply_text("✅ Session imported successfully! Now you can use `/dl` without logging in again.")


