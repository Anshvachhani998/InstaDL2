import motor.motor_asyncio
import os
from info import MONGO_URI, MONGO_NAME


class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_NAME]
        self.col = self.db["users"]

   
    async def add_user(self, id, name):
        """Add user to database if not exists"""
        if not await self.is_user_exist(id):
            user = self.new_user(id, name)
            await self.col.insert_one(user)
            return True
        return False

    async def is_user_exist(self, id):
        """Check if user already exists"""
        user = await self.col.find_one({"id": int(id)})
        return bool(user)


db = Database()
