import os

SESSION = "my_bot"
API_ID = int(os.getenv("API_ID", "8012239"))
API_HASH = os.getenv("API_HASH", "171e6f1bf66ed8dcc5140fbe827b6b08")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7277194738:AAHrewQsvKcPqeXYeMIbSk-nyUjgJ14kW8U")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002379643238"))
FORCE_CHANNEL = int(os.getenv("FORCE_CHANNEL", "-1002379643238"))
DUMP_CHANNEL = int(os.getenv("DUMP_CHANNEL", "-1002379643238"))
PORT = int(os.getenv("PORT", "8080"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Ansh089:Ansh089@cluster0.y8tpouc.mongodb.net/?retryWrites=true&w=majority")
MONGO_NAME = os.getenv("MONGO_NAME", "InstaDL")
ADMINS = [5961011848]
