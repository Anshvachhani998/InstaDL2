import instaloader
import os
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client  # Client ka object sahi se banao

# Instaloader Instance
L = instaloader.Instaloader()

USERNAME = "loveis8507"
SESSION_FILE = f"session-{USERNAME}"

otp_required = False  # OTP Flag
PASSWORD = None  # Store Password Temporarily

# ✅ /login <password> - Instagram Login Command
@app.on_message(filters.command("login"))
async def login_instagram(client, message: Message):
    global otp_required, PASSWORD, L
    
    if os.path.exists(SESSION_FILE):
        L.load_session_from_file(USERNAME)  # Session File Load Karo
        await message.reply_text("✅ Logged in using saved session!")
        return
    
    if len(message.command) < 2:
        await message.reply_text("❌ Usage: `/login <password>`")
        return

    PASSWORD = message.command[1]

    try:
        L.login(USERNAME, PASSWORD)
        L.save_session_to_file(SESSION_FILE)  # ✅ Session ko manually save karo
        await message.reply_text("✅ Login successful & session saved!")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        otp_required = True
        await message.reply_text("🔢 Enter OTP using `/otp <code>`")
    except Exception as e:
        await message.reply_text(f"❌ Login failed: {e}")

# ✅ /otp - Handle OTP Input
@app.on_message(filters.command("otp"))
async def handle_otp(client, message: Message):
    global otp_required, PASSWORD, L
    
    if not otp_required:
        await message.reply_text("❌ OTP is not required. Use /login first.")
        return
    
    if len(message.command) < 2:
        await message.reply_text("Usage: /otp <code>")
        return

    otp_code = message.command[1]

    try:
        L.two_factor_login(otp_code)
        L.save_session_to_file(SESSION_FILE)  # ✅ OTP Verify hone ke baad session save karo
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
