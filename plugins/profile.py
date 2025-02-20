from pyrogram import Client, filters
from plugins.auth import InstaClient





@Client.on_message(filters.command("profile"))
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
        📖 **Bio:** {bio}
        👥 **Followers:** {followers}
        🔄 **Following:** {following}
        """

        message.reply_photo(profile_pic, caption=response_text)
    except Exception as e:
        message.reply_text(f"❌ Error: {str(e)}")

