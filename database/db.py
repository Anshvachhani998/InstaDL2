import motor.motor_asyncio
from info import MONGO_URI, MONGO_NAME

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_NAME]
        self.col = self.db["users"]
        self.downloads_collection = self.db["downloads"]

    def new_user(self, id, name):
        return {"id": int(id), "name": name}
       
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):      
        user = await self.col.find_one({"id": int(id)})
        return bool(user)

    async def increment_download_count(self):
        await self.downloads_collection.update_one(
            {}, 
            {"$setOnInsert": {"total_downloads": 0}},
            upsert=True
        )
        
        await self.downloads_collection.update_one({}, {"$inc": {"total_downloads": 1}})

    async def get_all_users(self):
        return self.col.find({})

    async def get_total_downloads(self):  
        result = await self.db["downloads"].find_one({}, {"total_downloads": 1})
        if result:
            return result.get("total_downloads", 0)
        return 0
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def block_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

# Initialize database object
db = Database()
