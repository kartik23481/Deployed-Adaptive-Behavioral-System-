# # services/recommendation_service.py

# # Recommendation service for fetching similar items based on user behavior

# import math
# import os,json,numpy as np
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient
# from config import *
# from dotenv import load_dotenv
# load_dotenv()

# model=SentenceTransformer("all-MiniLM-L6-v2")

# # qdrant=QdrantClient(host=QDRANT_HOST,port=QDRANT_PORT) # local qdrant server

# # qdrant cloud
# qdrant = QdrantClient(
#     url=os.getenv("QDRANT_URL"),
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# def get_query_embedding(query):
#     return model.encode(query).tolist()


# def compute_weight(time_spent, click_count, scroll_depth):

#     time_norm = 1 - math.exp(-time_spent / 120.0)
#     click_norm = 1 - math.exp(-click_count / 5.0)
#     scroll_norm = 1 - math.exp(-scroll_depth / 200.0)

#     engagement_score = (
#         0.45 * time_norm +
#         0.45 * click_norm +
#         0.10 * scroll_norm
#     )

#     if time_spent < 10 and click_count == 0:
#         engagement_score *= 0.15

#     elif time_spent < 20 and click_count <= 1:
#         engagement_score *= 0.4

#     return float(min(engagement_score, 1.0))


# def get_past_embedding():
#     if os.path.exists(PAST_EMBEDDING_FILE):
#         with open(PAST_EMBEDDING_FILE,"r",encoding="utf-8") as f:
#             return json.load(f)

#     return [0.0]*EMBEDDING_SIZE

# # Saving embedding

# def save_past_embedding(embedding):
#     with open(PAST_EMBEDDING_FILE,"w",encoding="utf-8") as f:
#         json.dump(embedding,f)


# def update_user_embedding(query_embedding, past_embedding, weight):
#     query_embedding = np.array(query_embedding, dtype=np.float32)
#     past_embedding  = np.array(past_embedding,  dtype=np.float32)
    
#     updated = past_embedding + weight * query_embedding
    
#     return updated.tolist()

# # Qdrant Searching

# def search_similar_items(embedding):
#     results=qdrant.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=embedding,
#         limit=30,
#         with_payload=True
#     )
#     return [
#         hit.payload
#         for hit in results
#     ]







# # mongodb for single user handling
# # services/recommendation_service.py

# import math
# import os, json, numpy as np
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient
# from config import *
# from dotenv import load_dotenv
# load_dotenv()

# model = SentenceTransformer("all-MiniLM-L6-v2")

# qdrant = QdrantClient(
#     url=os.getenv("QDRANT_URL"),
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# def get_query_embedding(query):
#     return model.encode(query).tolist()

# def compute_weight(time_spent, click_count, scroll_depth):
#     time_norm = 1 - math.exp(-time_spent / 120.0)
#     click_norm = 1 - math.exp(-click_count / 5.0)
#     scroll_norm = 1 - math.exp(-scroll_depth / 200.0)
#     engagement_score = (
#         0.45 * time_norm +
#         0.45 * click_norm +
#         0.10 * scroll_norm
#     )
#     if time_spent < 10 and click_count == 0:
#         engagement_score *= 0.15
#     elif time_spent < 20 and click_count <= 1:
#         engagement_score *= 0.4
#     return float(min(engagement_score, 1.0))

# # ── NOW ASYNC, uses MongoDB ───────────────────────────────────────────────────

# async def get_past_embedding():
#     from services.mongo_store import get_past_user_embedding
#     result = await get_past_user_embedding()
#     return result if result else [0.0] * EMBEDDING_SIZE

# async def save_past_embedding(embedding):
#     from services.mongo_store import set_past_user_embedding
#     await set_past_user_embedding(embedding)

# def update_user_embedding(query_embedding, past_embedding, weight):
#     query_embedding = np.array(query_embedding, dtype=np.float32)
#     past_embedding  = np.array(past_embedding,  dtype=np.float32)
#     updated = past_embedding + weight * query_embedding
#     return updated.tolist()

# def search_similar_items(embedding):
#     results = qdrant.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=embedding,
#         limit=30,
#         with_payload=True
#     )
#     return [hit.payload for hit in results]






# mongodb for multi user handling
# services/recommendation_service.py

import math
import os, numpy as np
# from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from config import *
from dotenv import load_dotenv
load_dotenv()


qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# model = SentenceTransformer("all-MiniLM-L6-v2")
# def get_query_embedding(query):
#     return model.encode(query).tolist()


async def get_query_embedding(query: str, CATEGORY_EMBEDDINGS: dict):
    from services.search_service import get_query_embedding_from_category
    embedding, _ = await get_query_embedding_from_category(query, CATEGORY_EMBEDDINGS)
    return embedding if embedding else [0.0] * EMBEDDING_SIZE

def compute_weight(time_spent, click_count, scroll_depth):
    time_norm = 1 - math.exp(-time_spent / 120.0)
    click_norm = 1 - math.exp(-click_count / 5.0)
    scroll_norm = 1 - math.exp(-scroll_depth / 200.0)
    engagement_score = (
        0.45 * time_norm +
        0.45 * click_norm +
        0.10 * scroll_norm
    )
    if time_spent < 10 and click_count == 0:
        engagement_score *= 0.15
    elif time_spent < 20 and click_count <= 1:
        engagement_score *= 0.4
    return float(min(engagement_score, 1.0))

async def get_past_embedding(user_id: str):
    from services.mongo_store import get_past_user_embedding
    result = await get_past_user_embedding(user_id)
    return result if result else [0.0] * EMBEDDING_SIZE

async def save_past_embedding(user_id: str, embedding):
    from services.mongo_store import set_past_user_embedding
    await set_past_user_embedding(user_id, embedding)

def update_user_embedding(query_embedding, past_embedding, weight):
    query_embedding = np.array(query_embedding, dtype=np.float32)
    past_embedding  = np.array(past_embedding,  dtype=np.float32)
    updated = past_embedding + weight * query_embedding
    return updated.tolist()

def search_similar_items(embedding):
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=30,
        with_payload=True
    )
    return [hit.payload for hit in results]










# # Recommendation service for fetching similar items based on user behavior

# import os, json, numpy as np
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient
# from datetime import datetime
# from config import *
# from models.schema import UserBehavior

# model = SentenceTransformer("all-MiniLM-L6-v2")
# qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# def get_query_embedding(query):
#     return model.encode(query).tolist()

# def compute_weight(t, c, s):
#     raw = ALPHA*t + BETA*c + GAMMA*s
#     sig = 1/(1+np.exp(-raw))
#     return sig - 0.5

# def get_past_embedding():
#     if os.path.exists(PAST_EMBEDDING_FILE):
#         return json.load(open(PAST_EMBEDDING_FILE))
#     return [0.0]*EMBEDDING_SIZE

# def save_past_embedding(v):
#     json.dump(v, open(PAST_EMBEDDING_FILE,"w"))

# def search_similar_items(v):
#     res = qdrant.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=v,
#         limit=30,
#         with_payload=True
#     )
#     return [hit.payload for hit in res]






