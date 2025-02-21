import os
from instagrapi import Client as InstaClient
from instagrapi.exceptions import LoginRequired

INSTAGRAM_SESSION_FILE = "session.json"

insta_client = InstaClient()
insta_client.delay_range = [3, 6]  

# ✅ Pehle session file load karne ki koshish karenge
if os.path.exists(INSTAGRAM_SESSION_FILE):
    try:
        insta_client.load_settings(INSTAGRAM_SESSION_FILE)
        insta_client.get_timeline_feed()  # ✅ Check if session is valid
        print("✅ Instagram session loaded successfully!")
    except LoginRequired:
        print("⚠️ Session expired. Logging in again...")
        insta_client.login("harshvi_039", "Ansh123@123")
        insta_client.dump_settings(INSTAGRAM_SESSION_FILE)  # ✅ Save new session
else:
    print("⚠️ No session file found. Logging in...")
    insta_client.login("harshvi_039", "Ansh123@123")
    insta_client.dump_settings(INSTAGRAM_SESSION_FILE)  # ✅ Save session
