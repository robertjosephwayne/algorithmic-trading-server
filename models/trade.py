import motor.motor_asyncio
import os
import pydantic
from bson.objectid import ObjectId

db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = db_client.development
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class Trade:
    @staticmethod
    async def get_history():
        history = await db["trades"].find().to_list(1000)
        return history
