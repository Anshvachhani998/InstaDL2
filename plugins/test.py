import requests
from pyrogram import filters
from pyrogram import Client as bot
from instagrapi import Client as InstaClient
import os

# Initialize Instagram Client
INSTAGRAM_SESSION_FILE = "session.json"
insta_client = InstaClient()

# Load session if exists
if os.path.exists(INSTAGRAM_SESSION_FILE):
    insta_client.load_settings(INSTAGRAM_SESSION_FILE)
else:
    insta_client.login("loveis8507", "Ansh12345@23")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)


@bot.on_message(filters.command("profile"))
def profile_command(client, message):
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
        📚 **Bio:** {bio}
        👥 **Followers:** {followers}
        🔄 **Following:** {following}
        """

        # Download the profile picture
        img_data = requests.get(profile_pic).content
        img_path = f"{username}_profile.jpg"
        with open(img_path, "wb") as f:
            f.write(img_data)

        # Send the image
        message.reply_photo(img_path, caption=response_text)

        # Remove the downloaded image to save space
        os.remove(img_path)

    except Exception as e:
        message.reply_text(f"❌ Error: {str(e)}")
