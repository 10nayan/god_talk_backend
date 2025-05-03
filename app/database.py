from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

MONGODB_URI = settings.MONGODB_URI  # Should be a MongoDB URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_default_database()  # Or specify db name: client["your_db_name"]

# Dependency for FastAPI
async def get_database():
    return db