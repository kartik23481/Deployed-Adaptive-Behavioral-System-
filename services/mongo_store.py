# # for single user handling

# from db import get_db

# # ── CATEGORY EMBEDDINGS ───────────────────────────────────────────────────────

# async def get_all_category_embeddings():
#     db = get_db()
#     docs = await db.category_embeddings.find({}, {"_id": 0}).to_list(None)
#     return {d["category"]: d for d in docs}

# async def upsert_similarity_scores(scores: list):
#     db = get_db()
#     for s in scores:
#         await db.category_similarity.replace_one(
#             {"category": s["category"]}, s, upsert=True
#         )

# async def get_category_similarity_scores():
#     db = get_db()
#     return await db.category_similarity.find(
#         {}, {"_id": 0}
#     ).sort("score", -1).to_list(None)

# # ── DISPLAY ───────────────────────────────────────────────────────────────────

# async def get_display_products():
#     db = get_db()
#     return await db.display.find({}, {"_id": 0}).to_list(None)

# # ── PAST USER EMBEDDING ───────────────────────────────────────────────────────

# async def get_past_user_embedding():
#     db = get_db()
#     doc = await db.past_user_embedding.find_one({"_id": "singleton"})
#     return doc["embedding"] if doc else None

# async def set_past_user_embedding(embedding: list):
#     db = get_db()
#     await db.past_user_embedding.replace_one(
#         {"_id": "singleton"},
#         {"_id": "singleton", "embedding": embedding},
#         upsert=True
#     )

# # ── POPULAR PRODUCTS ──────────────────────────────────────────────────────────

# async def get_popular_products():
#     db = get_db()
#     return await db.popular_products.find({}, {"_id": 0}).to_list(None)

# async def set_popular_products(products: list):
#     db = get_db()
#     await db.popular_products.drop()
#     if products:
#         await db.popular_products.insert_many(products)

# # ── SESSION META ──────────────────────────────────────────────────────────────

# async def get_session_meta():
#     db = get_db()
#     doc = await db.session_meta.find_one({"_id": "singleton"})
#     return {k: v for k, v in doc.items() if k != "_id"} if doc else {}

# async def set_session_meta(data: dict):
#     db = get_db()
#     await db.session_meta.replace_one(
#         {"_id": "singleton"},
#         {"_id": "singleton", **data},
#         upsert=True
#     )

# # ── USER BEHAVIOR LOG ─────────────────────────────────────────────────────────

# async def append_behavior_log(entry: dict):
#     db = get_db()
#     await db.user_behavior_log.insert_one(entry)

# async def get_behavior_log():
#     db = get_db()
#     return await db.user_behavior_log.find(
#         {}, {"_id": 0}
#     ).sort("timestamp", -1).to_list(None)

# # ── USER INTEREST ─────────────────────────────────────────────────────────────

# async def get_user_interest():
#     db = get_db()
#     return await db.user_interest.find({}, {"_id": 0}).to_list(None)

# async def set_user_interest(products: list):
#     db = get_db()
#     await db.user_interest.drop()
#     if products:
#         await db.user_interest.insert_many(products)

# # ── PRODUCTS ──────────────────────────────────────────────────────────────────

# async def get_products_by_season_category(season: str, category: str):
#     db = get_db()
#     return await db.products.find(
#         {"season": season, "category": category}, {"_id": 0}
#     ).to_list(None)

# async def get_products_by_season(season: str):
#     db = get_db()
#     return await db.products.find(
#         {"season": season}, {"_id": 0}
#     ).to_list(None)

# # ── SCRAPE CACHE ──────────────────────────────────────────────────────────────

# async def get_last_scraped_query():
#     db = get_db()
#     doc = await db.scrape_cache.find_one({"_id": "last_query"})
#     return doc.get("query", "") if doc else ""

# async def set_last_scraped_query(query: str):
#     db = get_db()
#     await db.scrape_cache.replace_one(
#         {"_id": "last_query"},
#         {"_id": "last_query", "query": query},
#         upsert=True
#     )

# async def get_scraped_products():
#     db = get_db()
#     return await db.scrape_cache.find(
#         {"_id": {"$ne": "last_query"}}, {"_id": 0}
#     ).to_list(None)

# async def set_scraped_products(products: list):
#     db = get_db()
#     await db.scrape_cache.delete_many({"_id": {"$ne": "last_query"}})
#     if products:
#         await db.scrape_cache.insert_many(products)



# for multi users handling

from db import get_db

# ── STATIC (no user_id) ───────────────────────────────────────────────────────

async def get_all_category_embeddings():
    db = get_db()
    docs = await db.category_embeddings.find({}, {"_id": 0}).to_list(None)
    return {d["category"]: d for d in docs}

async def get_display_products():
    db = get_db()
    return await db.display.find({}, {"_id": 0}).to_list(None)

async def get_products_by_season_category(season: str, category: str):
    db = get_db()
    return await db.products.find(
        {"season": season, "category": category}, {"_id": 0}
    ).to_list(None)

async def get_products_by_season(season: str):
    db = get_db()
    return await db.products.find({"season": season}, {"_id": 0}).to_list(None)

# ── SCRAPE CACHE (global) ─────────────────────────────────────────────────────

# async def get_last_scraped_query():
#     db = get_db()
#     doc = await db.scrape_cache.find_one({"_id": "last_query"})
#     return doc.get("query", "") if doc else ""

# async def set_last_scraped_query(query: str):
#     db = get_db()
#     await db.scrape_cache.replace_one(
#         {"_id": "last_query"},
#         {"_id": "last_query", "query": query},
#         upsert=True
#     )


# async def get_last_scraped_query():
#     db = get_db()
#     doc = await db.scrape_cache.find_one({"_id": "last_query"})
#     if not doc:
#         return {"query": "", "parent_cat": "", "sub_cat": ""}
#     return {
#         "query": doc.get("query", ""),
#         "parent_cat": doc.get("parent_cat", ""),
#         "sub_cat": doc.get("sub_cat", "")
#     }

# async def set_last_scraped_query(query: str, parent_cat: str, sub_cat: str):
#     db = get_db()
#     await db.scrape_cache.replace_one(
#         {"_id": "last_query"},
#         {"_id": "last_query", "query": query, "parent_cat": parent_cat, "sub_cat": sub_cat},
#         upsert=True
#     )


# async def get_scraped_products():
#     db = get_db()
#     return await db.scrape_cache.find(
#         {"_id": {"$ne": "last_query"}}, {"_id": 0}
#     ).to_list(None)

# async def set_scraped_products(products: list):
#     db = get_db()
#     await db.scrape_cache.delete_many({"_id": {"$ne": "last_query"}})
#     if products:
#         await db.scrape_cache.insert_many(products)


async def is_query_scraped(query: str) -> bool:
    db = get_db()
    doc = await db.scraped_products.find_one({"query": query}, {"_id": 1})
    return doc is not None

async def get_scraped_products(query: str):
    db = get_db()
    doc = await db.scraped_products.find_one({"query": query}, {"products": 1, "_id": 0})
    return doc.get("products", []) if doc else []

from datetime import datetime, timezone

async def set_scraped_products(query: str, parent_cat: str, sub_cat: str, products: list):
    db = get_db()
    await db.scraped_products.replace_one(
        {"query": query},
        {
            "query": query,
            "parent_cat": parent_cat,
            "sub_cat": sub_cat,
            "products": products,
            "scraped_at": datetime.now(timezone.utc)
        },
        upsert=True
    )

# ── CATEGORY SIMILARITY (per user) ───────────────────────────────────────────

async def upsert_similarity_scores(user_id: str, scores: list):
    db = get_db()
    for s in scores:
        await db.category_similarity.replace_one(
            {"user_id": user_id, "category": s["category"]},
            {"user_id": user_id, **s},
            upsert=True
        )

async def get_category_similarity_scores(user_id: str):
    db = get_db()
    return await db.category_similarity.find(
        {"user_id": user_id}, {"_id": 0, "user_id": 0}
    ).sort("score", -1).to_list(None)

# ── PAST USER EMBEDDING (per user) ───────────────────────────────────────────

async def get_past_user_embedding(user_id: str):
    db = get_db()
    doc = await db.past_user_embedding.find_one({"_id": user_id})
    return doc["embedding"] if doc else None

async def set_past_user_embedding(user_id: str, embedding: list):
    db = get_db()
    await db.past_user_embedding.replace_one(
        {"_id": user_id},
        {"_id": user_id, "embedding": embedding},
        upsert=True
    )

# ── POPULAR PRODUCTS (per user) ───────────────────────────────────────────────

async def get_popular_products(user_id: str):
    db = get_db()
    return await db.popular_products.find(
        {"user_id": user_id}, {"_id": 0, "user_id": 0}
    ).to_list(None)

async def set_popular_products(user_id: str, products: list):
    db = get_db()
    await db.popular_products.delete_many({"user_id": user_id})
    if products:
        await db.popular_products.insert_many(
            [{"user_id": user_id, **p} for p in products]
        )

# ── SESSION META (per user) ───────────────────────────────────────────────────

async def get_session_meta(user_id: str):
    db = get_db()
    doc = await db.session_meta.find_one({"_id": user_id})
    return {k: v for k, v in doc.items() if k != "_id"} if doc else {}

async def set_session_meta(user_id: str, data: dict):
    db = get_db()
    await db.session_meta.replace_one(
        {"_id": user_id},
        {"_id": user_id, **data},
        upsert=True
    )

# ── USER BEHAVIOR LOG (per user) ──────────────────────────────────────────────

async def append_behavior_log(user_id: str, entry: dict):
    db = get_db()
    await db.user_behavior_log.insert_one({"user_id": user_id, **entry})

async def get_behavior_log(user_id: str):
    db = get_db()
    return await db.user_behavior_log.find(
        {"user_id": user_id}, {"_id": 0, "user_id": 0}
    ).sort("timestamp", -1).to_list(None)

# ── USER INTEREST (per user) ──────────────────────────────────────────────────

async def get_user_interest(user_id: str):
    db = get_db()
    return await db.user_interest.find(
        {"user_id": user_id}, {"_id": 0, "user_id": 0}
    ).to_list(None)

async def set_user_interest(user_id: str, products: list):
    db = get_db()
    await db.user_interest.delete_many({"user_id": user_id})
    if products:
        await db.user_interest.insert_many(
            [{"user_id": user_id, **p} for p in products]
        )