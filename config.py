# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# BASE_DIR = os.path.dirname(__file__)
# STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# DISPLAY_FILE = os.path.join(STORAGE_DIR, "display.json")
# USER_INTEREST_FILE = os.path.join(STORAGE_DIR, "user_interest.json")
# PAST_EMBEDDING_FILE = os.path.join(STORAGE_DIR, "past_user_embedding.json")
# SESSION_META_FILE = os.path.join(STORAGE_DIR, "session_meta.json")
# LOG_FILE = os.path.join(STORAGE_DIR, "user_behavior_log.json")
# SCRAPED_FILE = os.path.join(STORAGE_DIR, "scraped_products.json")
# LAST_QUERY_FILE = os.path.join(STORAGE_DIR, "last_scraped_query.json")

# Embedding / decay
EMBEDDING_SIZE = 384
LAMBDA = 0.30

# Behavior weights
# ALPHA = 0.7
# BETA = 0.6
# GAMMA = 0.3

# Qdrant
COLLECTION_NAME = "Smartcart_products"
# QDRANT_HOST = "localhost"
# QDRANT_PORT = 6333


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "ecom_behavioral")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
# Safe integer parsing that handles empty strings gracefully
jwt_expire_env = os.getenv("JWT_EXPIRE_MINUTES")
if jwt_expire_env and jwt_expire_env.strip():
    JWT_EXPIRE_MINUTES = int(jwt_expire_env)
else:
    JWT_EXPIRE_MINUTES = 10080  # Default fallback fallback