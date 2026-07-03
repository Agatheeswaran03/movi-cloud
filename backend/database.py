from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# MongoDB async client
client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
db = client[settings.DATABASE_NAME]

# Collection references
users_collection = db["users"]
tasks_collection = db["tasks"]


async def connect_db():
    """Verify MongoDB connection and ensure the database is reachable."""
    await client.admin.command("ping")


def close_db():
    """Close the MongoDB client cleanly."""
    client.close()


async def create_indexes():
    """Create database indexes for performance and uniqueness constraints."""
    # Unique index on email for users
    await users_collection.create_index("email", unique=True)
    # Compound index on user_id for task queries
    await tasks_collection.create_index("user_id")
