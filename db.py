from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI, MONGODB_DB

client: AsyncIOMotorClient = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGODB_DB]
    await create_indexes()
    print("✅ MongoDB connected")

async def close_db():
    if client:
        client.close()

def get_db():
    return db

async def create_indexes():
    d = get_db()
    await d.products.create_index([("season", 1), ("category", 1)])
    await d.category_embeddings.create_index([("category", 1)], unique=True)
    await d.users.create_index([("google_id", 1)], unique=True)
    await d.users.create_index([("email", 1)], unique=True)
    await d.category_similarity.create_index([("user_id", 1), ("category", 1)], unique=True)
    await d.past_user_embedding.create_index([("_id", 1)])
    await d.popular_products.create_index([("user_id", 1)])
    await d.session_meta.create_index([("_id", 1)])
    await d.user_behavior_log.create_index([("user_id", 1), ("timestamp", -1)])
    await d.user_interest.create_index([("user_id", 1)])
    await d.scraped_products.create_index([("query", 1)], unique=True)
    await d.scraped_products.create_index([("scraped_at", 1)],expireAfterSeconds=86400 )