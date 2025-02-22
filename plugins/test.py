from pyrogram import Client, filters
from instagrapi import Client as InstaClient
import os

# Initialize Pyrogram Bot
bot = Client

INSTAGRAM_SESSION_FILE = "session.json"
insta_client = InstaClient()

def ensure_logged_in():
    """ Ensure Instagram is logged in before making requests """
    if os.path.exists(INSTAGRAM_SESSION_FILE):
        try:
            with open(INSTAGRAM_SESSION_FILE, "r") as f:
                session_data = f.read()
                insta_client.load_settings(session_data)  
            if insta_client.get_settings():
                return  # ✅ Already logged in
        except Exception as e:
            print(f"⚠️ Session Load Failed: {e}")

    insta_client.login("loveis8507", "Ansh12345@23")

    with open(INSTAGRAM_SESSION_FILE, "w") as f:
        f.write(insta_client.dump_settings())  # ✅ FIXED: No argument needed


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
async def handle_document_upload(client, message):
    """ Handles session.json file upload """
    document = message.document
    if document.file_name == "session.json":
        file_path = await client.download_media(message)  # ✅ FIXED: `await` and `client`
        
        try:
            insta_client.load_settings(file_path)  # ✅ Validate session before saving
            os.rename(file_path, INSTAGRAM_SESSION_FILE)
            message.reply_text("✅ Session file imported successfully & validated!")
        except Exception:
            message.reply_text("❌ Invalid session file. Please try again.")
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




@bot.on_message(filters.command("p"))
def profile_sncommand(client, message):
    if len(message.command) < 2:
        message.reply_text("⚠️ Please provide a username: `/profile <username>`")
        return

    username = message.command[1]
    
    try:
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
