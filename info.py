import os

SESSION = "my_bot"
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))
PORT = int(os.getenv("PORT", "8080"))
