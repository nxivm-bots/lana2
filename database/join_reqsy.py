import motor.motor_asyncio
from config import FORCE_SUB_CHANNEL2



class JoinReqsy:

    def __init__(self):
        from config import JOIN_REQ_DB
        if JOIN_REQ_DB:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQ_DB)
            self.jishuboty = self.client["JoinRequesty"]
            self.col = self.jishuboty[str(FORCE_SUB_CHANNEL2)]
        else:
            self.client = None
            self.jishuboty = None
            self.col = None

    def isActive(self):
        if self.client is not None:
            return True
        else:
            return False

    async def add_user(self, user_id, first_name, username, date):
        try:
            await self.col.insert_one({"_id": int(user_id),"user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
        except:
            pass

    async def get_user(self, user_id):
        return await self.col.find_one({"user_id": int(user_id)})

    async def get_all_users(self):
        return await self.col.find().to_list(None)

    async def delete_user(self, user_id):
        await self.col.delete_one({"user_id": int(user_id)})

    async def delete_all_users(self):
        await self.col.delete_many({})

    async def get_all_users_count(self):
        return await self.col.count_documents({})
