import os
import json
from instagrapi import Client as InstaClient
from instagrapi.exceptions import LoginRequired
from info import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD  # Credentials alag file me rakho

SESSION_FILE = "session.json"
insta_client = InstaClient()
insta_client.delay_range = [3, 6]  # Requests slow karne ke liye

# ✅ Instagram Session Load/ Login Handle
def login():
    if os.path.exists(SESSION_FILE):
        try:
            insta_client.load_settings(SESSION_FILE)  # Session file load karega
            insta_client.get_timeline_feed()  # Check karega ki session valid hai ya expire ho gaya
            return "✅ Logged in using session file."
        except LoginRequired:
            return "⚠️ Session expired. Please use /login to log in again."

    # Agar session file nahi mili, toh login karega
    try:
        insta_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        insta_client.dump_settings(SESSION_FILE)
        return "✅ Login successful! Session saved."
    except Exception as e:
        return f"❌ Login failed: {str(e)}"

# ✅ Session Check Function (Har command me use karne ke liye)
def check_session():
    try:
        insta_client.get_timeline_feed()  # Instagram pe request bhej kar session validity check karega
        return True
    except LoginRequired:
        return False
      
