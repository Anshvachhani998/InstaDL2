import json
from pyrogram import Client, filters
from instagrapi import Client as InstaClient
from instagrapi.exceptions import LoginRequired, ChallengeRequired
from info import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD  # Credentials alag file me rakho



cl = InstaClient()
cl.delay_range = [3, 6]  


@bot.on_message(filters.command("login"))
def instagram_login(client, message):
    user_id = message.from_user.id
    message.reply_text("🔄 Checking Instagram session...")

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.get_timeline_feed()
            message.reply_text("✅ Already logged in using session file.")
            return
        except LoginRequired:
            message.reply_text("⚠️ Session expired. Logging in again...")

    try:
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        cl.dump_settings(SESSION_FILE)
        message.reply_text("✅ Login successful! Session saved.")
    except ChallengeRequired:
        message.reply_text("⚠️ Instagram requires OTP. Check your email/SMS and use /otp <code> to proceed.")

@bot.on_message(filters.command("otp"))
def handle_otp(client, message):
    otp_code = message.text.split(" ", 1)[-1].strip()
    if not otp_code.isdigit() or len(otp_code) != 6:
        message.reply_text("❌ Invalid OTP. Please enter a 6-digit OTP like: `/otp 123456`")
        return

    try:
        cl.challenge_code_handler = lambda username, choice: otp_code
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        cl.dump_settings(SESSION_FILE)
        message.reply_text("✅ OTP verified, login successful!")
    except Exception as e:
        message.reply_text(f"❌ OTP failed: {str(e)}")
