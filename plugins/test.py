from pyrogram import Client, filters
from instagrapi import Client as InstaClient
import os

# Initialize Pyrogram Bot
bot = Client

INSTAGRAM_SESSION_FILE = "session.json"
insta_client = InstaClient()

def ensure_logged_in():
    """ Ensure Instagram is logged in before making requests """
    if insta_client.get_settings():  
        return  # Already logged in

    if os.path.exists(INSTAGRAM_SESSION_FILE):
        try:
            insta_client.load_settings(INSTAGRAM_SESSION_FILE)
        except Exception:
            pass  # Ignore errors and proceed to login

    if not insta_client.get_settings():  # If still not logged in
        insta_client.login("loveis8507", "Ansh12345@23")
        insta_client.dump_settings(INSTAGRAM_SESSION_FILE)

@bot.on_message(filters.command("export_session"))
def export_session(client, message):
    """ Exports the current session.json file """
    if os.path.exists(INSTAGRAM_SESSION_FILE):
        message.reply_document(INSTAGRAM_SESSION_FILE, caption="✅ Here is your Instagram session file.")
    else:
        message.reply_text("⚠️ No session file found. Please login using `/login` first.")

@bot.on_message(filters.command("import_session"))
def import_session(client, message):
    """ Prompts user to upload a session file """
    message.reply_text("📥 Please send your `session.json` file.")

@bot.on_message(filters.document)
def handle_document_upload(client, message):
    """ Handles session.json file upload """
    document = message.document
    if document.file_name == "session.json":
        file_path = bot.download_media(message)
        os.rename(file_path, INSTAGRAM_SESSION_FILE)
        message.reply_text("✅ Session file imported successfully!")
    else:
        message.reply_text("⚠️ Invalid file. Please send `session.json`.")

@bot.on_message(filters.command("profile"))
def profile_command(client, message):
    if len(message.command) < 2:
        message.reply_text("⚠️ Please provide a username: `/profile <username>`")
        return

    username = message.command[1]

    try:
        ensure_logged_in()  # Ensure login before making request
        user_info = insta_client.user_info_by_username(username)
        profile_pic = user_info.profile_pic_url
        bio = user_info.biography or "No bio available."
        followers = user_info.follower_count
        following = user_info.following_count

        response_text = f"""
📌 **Instagram Profile Info**
👤 **Username:** {username}
📖 **Bio:** {bio}
👥 **Followers:** {followers}
🔄 **Following:** {following}
        """

        message.reply_photo(profile_pic, caption=response_text)
    except Exception as e:
        message.reply_text(f"❌ Error: {str(e)}")


