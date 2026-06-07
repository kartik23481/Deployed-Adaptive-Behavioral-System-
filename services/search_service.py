# # services/search_service.py

# # category detection and product search service using Google Gemini API

# import os
# import re
# import json
# import random
# import aiofiles
# from google import genai

# from config import STORAGE_DIR, SCRAPED_FILE, LAST_QUERY_FILE
# from domain.categories import dict1, dict2, seasonal_categories
# from services.scrape_service import scrape_flipkart_query
# from models.schema import NewProduct
# from fastapi import Query, HTTPException
# from dotenv import load_dotenv
# load_dotenv()
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# # Make sure your seasonal_categories dictionary is already defined
# # seasonal_categories = { "evergreen_categories": {...}, "summer_categories": {...} }

# async def detect_query_category(query: str) -> dict:
#     dict1 = {
#         "evergreen_categories": list(seasonal_categories["evergreen_categories"].keys()),
#         "summer_categories": list(seasonal_categories["summer_categories"].keys()),
#         "rainy_categories": list(seasonal_categories["rainy_categories"].keys()),
#         "winter_categories": list(seasonal_categories["winter_categories"].keys())
#     }

#     # Initialize the client once per process (not per request)
#     client = genai.Client(api_key=GEMINI_KEY)

#     evergreen_list = "\n".join(f"- {item}" for item in dict1["evergreen_categories"])
#     summer_list = "\n".join(f"- {item}" for item in dict1["summer_categories"])
#     rainy_list = "\n".join(f"- {item}" for item in dict1["rainy_categories"])
#     winter_list = "\n".join(f"- {item}" for item in dict1["winter_categories"])

#     prompt = f"""
# You are a category detection system for an AI-powered e-commerce platform.

# Your task is to:
# 1. Decide the parent category: either "evergreen_categories" or "summer_categories" or "rainy_categories" or "winter_categories"
# 2. Choose the correct sub-category from the list provided.
# 3. Do NOT invent new categories.
# 4. Return ONLY a JSON object in the following format (without explanations or markdown): 
# {{ "parent_category": "...", "sub_category": "..." }}

# Sub-categories you can choose from:

# Evergreen Categories:
# {evergreen_list}

# Summer Categories:
# {summer_list}

# Rainy Categories:
# {rainy_list}

# Winter Categories:
# {winter_list}

# Query: "{query.strip()}"

# If the query doesn't clearly match anything, return:
# {{ "parent_category": "unknown", "sub_category": "unknown" }}
# """

#     try:
#         # Use the new generate_content() method
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#         category_info = response.text.strip()

#         # Extract JSON block safely
#         match = re.search(r'\{[\s\S]*?\}', category_info)
#         if match:
#             category_info = match.group(0)
#             return json.loads(category_info)
#         else:
#             raise ValueError("No valid JSON returned by Gemini")

#     except Exception as e:
#         print("❌ Error from Gemini category detection:", e)
#         return {"parent_category": "unknown", "sub_category": "unknown"}



# async def search_products(
#     query: str = Query(..., min_length=1),
#     offset: int = Query(0, ge=0),
#     limit: int = Query(12, ge=1)
# ):
#     query = query.strip().lower()
#     matched_category = None
#     for cat_key, synonyms in dict2.items():
#         if query in synonyms:
#             matched_category = cat_key
#             break

#     if (matched_category):
    
#         parent_folder = None
#         for folder, categories in dict1.items():
#             if matched_category in categories:
#                 parent_folder = folder
#                 break

#         if not parent_folder:
#             raise HTTPException(status_code=404, detail="Matching folder not found.")

#         BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#         PROJECT_ROOT = os.path.dirname(BASE_DIR)

#         json_file_path = os.path.join(PROJECT_ROOT, "database" ,parent_folder, f"{matched_category}.json")

#         if not os.path.exists(json_file_path):
#             raise HTTPException(status_code=404, detail="Product file not found.")

#         try:
#             async with aiofiles.open(json_file_path, "r", encoding="utf-8") as f:
#                 content = await f.read()
#                 data = json.loads(content)

#             random.shuffle(data)

#             # Cyclic pagination function
#             def cyclic_slice(data, offset, limit):
#                 n = len(data)
#                 result = []
#                 for i in range(limit):
#                     index = (offset + i) % n  # Wrap around using modulo
#                     result.append(data[index])
#                 return result

#             paginated = cyclic_slice(data, offset, limit)

#             return [NewProduct(**item) for item in paginated]
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to load products: {str(e)}")

#     # ✅ Try product-specific handling (Part-2 query)
#     else:
#         try:
#             category_info = await detect_query_category(query)
#             parent_cat = category_info.get("parent_category", "unknown")
#             sub_cat = category_info.get("sub_category", "unknown")

#             if parent_cat != "unknown" and sub_cat != "unknown":
#                 category_key = sub_cat
#                 category_details = seasonal_categories.get(parent_cat, {}).get(category_key)

#                 if category_details:
#                     # 🔍 Check last query
#                     last_scraped_query = ""
#                     if os.path.exists(LAST_QUERY_FILE):
#                         async with aiofiles.open(LAST_QUERY_FILE, "r", encoding="utf-8") as f:
#                             try:
#                                 content = await f.read()
#                                 last_scraped_query = json.loads(content).get("query", "").strip().lower()
#                             except:
#                                 pass

#                     # 🧠 Only scrape if scrape_query is different
#                     if query != last_scraped_query :
#                         print(f"📡 Scraping because scraping_query is new: '{query}'")
#                         await scrape_flipkart_query(
#                             query=query,
#                             category_name=category_key,
#                             selector_type=category_details["selector_type"],
#                             selector_value=category_details["selector_value"],
#                             max_items=10
#                         )

#                         # 📂 Update last_scraped_query file
#                         async with aiofiles.open(LAST_QUERY_FILE, "w", encoding="utf-8") as f:
#                             await f.write(json.dumps({"query": query}))

#                     else:
#                         print(f"✅ Using cached data for last scraped_query: '{query}'")

#                     # 📂 Load products
#                     async with aiofiles.open(SCRAPED_FILE, "r", encoding="utf-8") as f:
#                         content = await f.read()
#                         data = json.loads(content)

#                     random.shuffle(data)

#                     def cyclic_slice(data, offset, limit):
#                         n = len(data)
#                         return [data[(offset + i) % n] for i in range(limit)]

#                     paginated = cyclic_slice(data, offset, limit)
#                     return [NewProduct(**item) for item in paginated]

#         except Exception as e:
#             print(f"❌ Error during category detection or scraping: {e}")

#     # ❌ Nothing found or failed
#     raise HTTPException(status_code=404, detail="No results found.")




# mongodb  (working)


# services/search_service.py

# import os
# import re
# import json
# import random
# from google import genai

# from domain.categories import dict1, dict2, seasonal_categories
# from services.scrape_service import scrape_flipkart_query
# from models.schema import NewProduct
# from fastapi import Query, HTTPException
# from dotenv import load_dotenv
# from services.mongo_store import (
#     get_products_by_season_category,
#     get_last_scraped_query,
#     set_last_scraped_query,
#     get_scraped_products
# )

# load_dotenv()
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")


# async def detect_query_category(query: str) -> dict:
#     d = {
#         "evergreen_categories": list(seasonal_categories["evergreen_categories"].keys()),
#         "summer_categories": list(seasonal_categories["summer_categories"].keys()),
#         "rainy_categories": list(seasonal_categories["rainy_categories"].keys()),
#         "winter_categories": list(seasonal_categories["winter_categories"].keys())
#     }

#     client = genai.Client(api_key=GEMINI_KEY)

#     evergreen_list = "\n".join(f"- {item}" for item in d["evergreen_categories"])
#     summer_list    = "\n".join(f"- {item}" for item in d["summer_categories"])
#     rainy_list     = "\n".join(f"- {item}" for item in d["rainy_categories"])
#     winter_list    = "\n".join(f"- {item}" for item in d["winter_categories"])

#     prompt = f"""
# You are a category detection system for an AI-powered e-commerce platform.

# Your task is to:
# 1. Decide the parent category: either "evergreen_categories" or "summer_categories" or "rainy_categories" or "winter_categories"
# 2. Choose the correct sub-category from the list provided.
# 3. Do NOT invent new categories.
# 4. Return ONLY a JSON object in the following format (without explanations or markdown): 
# {{ "parent_category": "...", "sub_category": "..." }}

# Sub-categories you can choose from:

# Evergreen Categories:
# {evergreen_list}

# Summer Categories:
# {summer_list}

# Rainy Categories:
# {rainy_list}

# Winter Categories:
# {winter_list}

# Query: "{query.strip()}"

# If the query doesn't clearly match anything, return:
# {{ "parent_category": "unknown", "sub_category": "unknown" }}
# """

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )
#         category_info = response.text.strip()
#         match = re.search(r'\{[\s\S]*?\}', category_info)
#         if match:
#             return json.loads(match.group(0))
#         raise ValueError("No valid JSON returned by Gemini")

#     except Exception as e:
#         print("❌ Gemini category detection error:", e)
#         return {"parent_category": "unknown", "sub_category": "unknown"}


# async def search_products(
#     query: str = Query(..., min_length=1),
#     offset: int = Query(0, ge=0),
#     limit: int = Query(12, ge=1)
# ):
#     query = query.strip().lower()

#     def cyclic_slice(data, offset, limit):
#         n = len(data)
#         return [data[(offset + i) % n] for i in range(limit)]

#     # ── Part 1: known category match ─────────────────────────────────────────
#     matched_category = None
#     for cat_key, synonyms in dict2.items():
#         if query in synonyms:
#             matched_category = cat_key
#             break

#     if matched_category:
#         parent_folder = None
#         for folder, categories in dict1.items():
#             if matched_category in categories:
#                 parent_folder = folder
#                 break

#         if not parent_folder:
#             raise HTTPException(status_code=404, detail="Matching folder not found.")

#         season = parent_folder.replace("_categories", "")
#         data = await get_products_by_season_category(season, matched_category)

#         if not data:
#             raise HTTPException(status_code=404, detail="Product file not found.")

#         random.shuffle(data)
#         paginated = cyclic_slice(data, offset, limit)
#         return [NewProduct(**item) for item in paginated]

#     # ── Part 2: Gemini detection + scrape ────────────────────────────────────
#     else:
#         try:
#             category_info = await detect_query_category(query)
#             parent_cat = category_info.get("parent_category", "unknown")
#             sub_cat    = category_info.get("sub_category", "unknown")

#             if parent_cat != "unknown" and sub_cat != "unknown":
#                 category_details = seasonal_categories.get(parent_cat, {}).get(sub_cat)

#                 if category_details:
#                     last_scraped_query = await get_last_scraped_query()

#                     if query != last_scraped_query:
#                         print(f"📡 Scraping new query: '{query}'")
#                         await scrape_flipkart_query(
#                             query=query,
#                             category_name=sub_cat,
#                             selector_type=category_details["selector_type"],
#                             selector_value=category_details["selector_value"],
#                             max_items=10
#                         )
#                         await set_last_scraped_query(query)
#                     else:
#                         print(f"✅ Using cached scrape for: '{query}'")

#                     data = await get_scraped_products()

#                     if not data:
#                         raise HTTPException(status_code=404, detail="No scraped products found.")

#                     random.shuffle(data)
#                     paginated = cyclic_slice(data, offset, limit)
#                     return [NewProduct(**item) for item in paginated]

#         except HTTPException:
#             raise
#         except Exception as e:
#             print(f"❌ Error during category detection or scraping: {e}")

#     raise HTTPException(status_code=404, detail="No results found.")








# # working
# # mongodb search service updated for removing allminilml6v2

# # services/search_service.py

# import os
# import re
# import json
# import random
# from google import genai

# from domain.categories import dict1, dict2, seasonal_categories
# from services.scrape_service import scrape_flipkart_query
# from models.schema import NewProduct
# from fastapi import Query, HTTPException
# from dotenv import load_dotenv
# from services.mongo_store import (
#     get_products_by_season_category,
#     get_last_scraped_query,
#     set_last_scraped_query,
#     get_scraped_products
# )

# load_dotenv()
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# import asyncio
# _scrape_lock = asyncio.Lock()


# def match_known_category(query: str):
#     """Returns (matched_category, parent_folder) or (None, None)"""
#     for cat_key, synonyms in dict2.items():
#         if query in synonyms:
#             for folder, categories in dict1.items():
#                 if cat_key in categories:
#                     return cat_key, folder
#             return cat_key, None
#     return None, None


# async def detect_query_category(query: str) -> dict:
#     d = {
#         "evergreen_categories": list(seasonal_categories["evergreen_categories"].keys()),
#         "summer_categories": list(seasonal_categories["summer_categories"].keys()),
#         "rainy_categories": list(seasonal_categories["rainy_categories"].keys()),
#         "winter_categories": list(seasonal_categories["winter_categories"].keys())
#     }
#     client = genai.Client(api_key=GEMINI_KEY)
#     evergreen_list = "\n".join(f"- {item}" for item in d["evergreen_categories"])
#     summer_list    = "\n".join(f"- {item}" for item in d["summer_categories"])
#     rainy_list     = "\n".join(f"- {item}" for item in d["rainy_categories"])
#     winter_list    = "\n".join(f"- {item}" for item in d["winter_categories"])

#     prompt = f"""
# You are a category detection system for an AI-powered e-commerce platform.
# Your task is to:
# 1. Decide the parent category: either "evergreen_categories" or "summer_categories" or "rainy_categories" or "winter_categories"
# 2. Choose the correct sub-category from the list provided.
# 3. Do NOT invent new categories.
# 4. Return ONLY a JSON object in the following format (without explanations or markdown): 
# {{ "parent_category": "...", "sub_category": "..." }}

# Evergreen Categories:\n{evergreen_list}
# Summer Categories:\n{summer_list}
# Rainy Categories:\n{rainy_list}
# Winter Categories:\n{winter_list}

# Query: "{query.strip()}"

# If the query doesn't clearly match anything, return:
# {{ "parent_category": "unknown", "sub_category": "unknown" }}
# """
#     try:
#         response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
#         category_info = response.text.strip()
#         match = re.search(r'\{[\s\S]*?\}', category_info)
#         if match:
#             return json.loads(match.group(0))
#         raise ValueError("No valid JSON returned by Gemini")
#     except Exception as e:
#         print("❌ Gemini category detection error:", e)
#         return {"parent_category": "unknown", "sub_category": "unknown"}


# async def get_query_embedding_from_category(query: str, CATEGORY_EMBEDDINGS: dict):
#     """
#     Returns (embedding, sub_cat) using category embeddings instead of sentence transformer.
#     embedding = None if category not found.
#     """
#     matched_category, _ = match_known_category(query)

#     if matched_category and matched_category in CATEGORY_EMBEDDINGS:
#         return CATEGORY_EMBEDDINGS[matched_category]["embedding"], matched_category

#     # Type 2 — use last scraped query's sub_cat
#     last = await get_last_scraped_query()
#     sub_cat = last.get("sub_cat", "")
#     if sub_cat and sub_cat in CATEGORY_EMBEDDINGS:
#         return CATEGORY_EMBEDDINGS[sub_cat]["embedding"], sub_cat

#     return None, None


# async def search_products(
#     query: str = Query(..., min_length=1),
#     offset: int = Query(0, ge=0),
#     limit: int = Query(12, ge=1)
# ):
#     query = query.strip().lower()

#     def cyclic_slice(data, offset, limit):
#         n = len(data)
#         return [data[(offset + i) % n] for i in range(limit)]

#     # ── Part 1: known category match ─────────────────────────────────────────
#     matched_category, parent_folder = match_known_category(query)

#     if matched_category:
#         if not parent_folder:
#             raise HTTPException(status_code=404, detail="Matching folder not found.")
#         season = parent_folder.replace("_categories", "")
#         data = await get_products_by_season_category(season, matched_category)
#         if not data:
#             raise HTTPException(status_code=404, detail="Product file not found.")
#         random.shuffle(data)
#         return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

#     # ── Part 2: Gemini detection + scrape ────────────────────────────────────
#     else:
#         try:
#             category_info = await detect_query_category(query)
#             parent_cat = category_info.get("parent_category", "unknown")
#             sub_cat    = category_info.get("sub_category", "unknown")

#             if parent_cat != "unknown" and sub_cat != "unknown":
#                 category_details = seasonal_categories.get(parent_cat, {}).get(sub_cat)

#                 if category_details:
#                     async with _scrape_lock:
#                         last = await get_last_scraped_query()

#                         if query != last.get("query", ""):
#                             print(f"📡 Scraping new query: '{query}'")
#                             await scrape_flipkart_query(
#                                 query=query,
#                                 category_name=sub_cat,
#                                 selector_type=category_details["selector_type"],
#                                 selector_value=category_details["selector_value"],
#                                 max_items=5
#                             )
#                             await set_last_scraped_query(query, parent_cat, sub_cat)
#                         else:
#                             print(f"✅ Using cached scrape for: '{query}'")

#                     data = await get_scraped_products()
#                     if not data:
#                         raise HTTPException(status_code=404, detail="No scraped products found.")
#                     random.shuffle(data)
#                     return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

#         except HTTPException:
#             raise
#         except Exception as e:
#             print(f"❌ Error during category detection or scraping: {e}")

#     raise HTTPException(status_code=404, detail="No results found.")






# totally working 
# # services/search_service.py

# import os
# import re
# import json
# import random
# import asyncio
# import httpx
# from google import genai

# from domain.categories import dict1, dict2, seasonal_categories
# from models.schema import NewProduct
# from fastapi import Query, HTTPException
# from dotenv import load_dotenv
# from services.scrape_service import scrape_flipkart_query
# from services.mongo_store import (
#     get_products_by_season_category,
#     is_query_scraped,
#     get_scraped_products,
#     set_scraped_products
# )

# load_dotenv()
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")
# from services.ws_manager import ws_manager

# # Replace _scrape_lock = asyncio.Lock() with:
# _scraper_semaphore = asyncio.Semaphore(1)
# _in_flight_scrapes = {}


# def match_known_category(query: str):
#     for cat_key, synonyms in dict2.items():
#         if query in synonyms:
#             for folder, categories in dict1.items():
#                 if cat_key in categories:
#                     return cat_key, folder
#             return cat_key, None
#     return None, None


# async def detect_query_category(query: str) -> dict:
#     d = {
#         "evergreen_categories": list(seasonal_categories["evergreen_categories"].keys()),
#         "summer_categories": list(seasonal_categories["summer_categories"].keys()),
#         "rainy_categories": list(seasonal_categories["rainy_categories"].keys()),
#         "winter_categories": list(seasonal_categories["winter_categories"].keys())
#     }
#     client = genai.Client(api_key=GEMINI_KEY)
#     evergreen_list = "\n".join(f"- {item}" for item in d["evergreen_categories"])
#     summer_list    = "\n".join(f"- {item}" for item in d["summer_categories"])
#     rainy_list     = "\n".join(f"- {item}" for item in d["rainy_categories"])
#     winter_list    = "\n".join(f"- {item}" for item in d["winter_categories"])

#     prompt = f"""
# You are a category detection system for an AI-powered e-commerce platform.
# Your task is to:
# 1. Decide the parent category: either "evergreen_categories" or "summer_categories" or "rainy_categories" or "winter_categories"
# 2. Choose the correct sub-category from the list provided.
# 3. Do NOT invent new categories.
# 4. Return ONLY a JSON object in the following format (without explanations or markdown): 
# {{ "parent_category": "...", "sub_category": "..." }}

# Evergreen Categories:\n{evergreen_list}
# Summer Categories:\n{summer_list}
# Rainy Categories:\n{rainy_list}
# Winter Categories:\n{winter_list}

# Query: "{query.strip()}"

# If the query doesn't clearly match anything, return:
# {{ "parent_category": "unknown", "sub_category": "unknown" }}
# """
#     try:
#         response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
#         category_info = response.text.strip()
#         match = re.search(r'\{[\s\S]*?\}', category_info)
#         if match:
#             return json.loads(match.group(0))
#         raise ValueError("No valid JSON returned by Gemini")
#     except Exception as e:
#         print("❌ Gemini category detection error:", e)
#         return {"parent_category": "unknown", "sub_category": "unknown"}


# async def get_query_embedding_from_category(query: str, CATEGORY_EMBEDDINGS: dict):
#     matched_category, _ = match_known_category(query)
#     if matched_category and matched_category in CATEGORY_EMBEDDINGS:
#         return CATEGORY_EMBEDDINGS[matched_category]["embedding"], matched_category
#     # Type 2 — find sub_cat from scraped_products
#     from services.mongo_store import get_db
#     db = get_db()
#     doc = await db.scraped_products.find_one(
#         {"query": query}, {"sub_cat": 1, "_id": 0}
#     )
#     if doc:
#         sub_cat = doc.get("sub_cat", "")
#         if sub_cat and sub_cat in CATEGORY_EMBEDDINGS:
#             return CATEGORY_EMBEDDINGS[sub_cat]["embedding"], sub_cat
#     return None, None


# async def search_products(
#     query: str = Query(..., min_length=1),
#     offset: int = Query(0, ge=0),
#     limit: int = Query(12, ge=1),
#     client_id: str = Query(..., description="Unique ID for the frontend client")
# ):
#     query = query.strip().lower()

#     def cyclic_slice(data, offset, limit):
#         n = len(data)
#         return [data[(offset + i) % n] for i in range(limit)]

#     # ── Part 1: known category match ─────────────────────────────────────────
#     matched_category, parent_folder = match_known_category(query)

#     if matched_category:
#         if not parent_folder:
#             raise HTTPException(status_code=404, detail="Matching folder not found.")
#         season = parent_folder.replace("_categories", "")
#         data = await get_products_by_season_category(season, matched_category)
#         if not data:
#             raise HTTPException(status_code=404, detail="Product file not found.")
#         random.shuffle(data)
#         return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

#     # ── Part 2: Type 2 query ──────────────────────────────────────────────────
#     else:
#         # ── Check if already scraped ──────────────────────────────────────────
#         already_scraped = await is_query_scraped(query)

#         if already_scraped:
#             print(f"✅ Cache hit — loading scraped products for: '{query}'")
#             data = await get_scraped_products(query)
#             if not data:
#                 raise HTTPException(status_code=404, detail="No scraped products found.")
#             random.shuffle(data)
#             return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

#         # ── Not scraped — detect category + scrape via ngrok ─────────────────
#         try:
#             # category_info = await detect_query_category(query)
#             # parent_cat = category_info.get("parent_category", "unknown")
#             # sub_cat    = category_info.get("sub_category", "unknown")
#             # testing terminal ui
#             parent_cat = "evergreen_categories" 
#             sub_cat    = "mobiles"
#             if parent_cat != "unknown" and sub_cat != "unknown":
#                 category_details = seasonal_categories.get(parent_cat, {}).get(sub_cat)

#                 if category_details:
                    
#                     # Deduplication: Wait if exact same query is already processing
#                     if query in _in_flight_scrapes:
#                         await ws_manager.send_personal_message("[SYSTEM] ⏳ Identical query in progress. Linking to stream...", client_id)
#                         await _in_flight_scrapes[query].wait()  # MUST HAVE .wait()
#                     else:
#                         current_scrape_event = asyncio.Event()
#                         _in_flight_scrapes[query] = current_scrape_event

#                         try:
#                             # Send wait message if queue is full
#                             if _scraper_semaphore.locked():
#                                 await ws_manager.send_personal_message("[SYSTEM] ⏳ System busy processing another request. You are in the queue...", client_id)

#                             async with _scraper_semaphore:
#                                 await ws_manager.send_personal_message("[SYSTEM] 🟢 Slot acquired! Launching extraction engine...", client_id)
#                                 print(f"📡 Scraping new query: '{query}'")
                                
#                                 # Pass client_id into scraper
#                                 scraped = await scrape_flipkart_query(
#                                     query=query,
#                                     category_name=sub_cat,
#                                     selector_type=category_details["selector_type"],
#                                     selector_value=category_details["selector_value"],
#                                     client_id=client_id,
#                                     max_items=5
#                                 )
                                
#                                 await set_scraped_products(query, parent_cat, sub_cat, scraped)
#                                 print(f"✅ Scraped {len(scraped)} products saved for: '{query}'")
                                
#                                 # Enforce 5-second cooldown before releasing semaphore
#                                 await ws_manager.send_personal_message("[SYSTEM] ⏱ Extraction complete. Cooling down network connections (5s)...", client_id)
#                                 await asyncio.sleep(5)
                        
#                         finally:
#                             _in_flight_scrapes.pop(query, None)
#                             current_scrape_event.set()

#                     data = await get_scraped_products(query)
#                     if not data:
#                         raise HTTPException(status_code=404, detail="No scraped products found.")
#                     random.shuffle(data)
#                     return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

#         except HTTPException:
#             raise
#         except Exception as e:
#             print(f"❌ Scraping error: {e}")

#     raise HTTPException(status_code=404, detail="No results found.")







# render + ngrok suppported 

# services/search_service.py (that run on render)

import os
import re
import json
import random
import asyncio
import httpx
from google import genai

from domain.categories import dict1, dict2, seasonal_categories
from models.schema import NewProduct
from fastapi import Query, HTTPException
from dotenv import load_dotenv

from services.mongo_store import (
    get_products_by_season_category,
    is_query_scraped,
    get_scraped_products,
    set_scraped_products
)

load_dotenv()
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")
from services.ws_manager import ws_manager

ACTIVE_WORKER_URL = os.getenv("NGROK_WORKER_URL", "")

_scraper_semaphore = asyncio.Semaphore(1)
_in_flight_scrapes = {}

# Keep match_known_category, detect_query_category, and get_query_embedding_from_category exactly as they are.

def match_known_category(query: str):
    for cat_key, synonyms in dict2.items():
        if query in synonyms:
            for folder, categories in dict1.items():
                if cat_key in categories:
                    return cat_key, folder
            return cat_key, None
    return None, None


# async def detect_query_category(query: str) -> dict:
#     d = {
#         "evergreen_categories": list(seasonal_categories["evergreen_categories"].keys()),
#         "summer_categories": list(seasonal_categories["summer_categories"].keys()),
#         "rainy_categories": list(seasonal_categories["rainy_categories"].keys()),
#         "winter_categories": list(seasonal_categories["winter_categories"].keys())
#     }
#     client = genai.Client(api_key=GEMINI_KEY)
#     evergreen_list = "\n".join(f"- {item}" for item in d["evergreen_categories"])
#     summer_list    = "\n".join(f"- {item}" for item in d["summer_categories"])
#     rainy_list     = "\n".join(f"- {item}" for item in d["rainy_categories"])
#     winter_list    = "\n".join(f"- {item}" for item in d["winter_categories"])

#     prompt = f"""
# You are a category detection system for an AI-powered e-commerce platform.
# Your task is to:
# 1. Decide the parent category: either "evergreen_categories" or "summer_categories" or "rainy_categories" or "winter_categories"
# 2. Choose the correct sub-category from the list provided.
# 3. Do NOT invent new categories.
# 4. Return ONLY a JSON object in the following format (without explanations or markdown): 
# {{ "parent_category": "...", "sub_category": "..." }}

# Evergreen Categories:\n{evergreen_list}
# Summer Categories:\n{summer_list}
# Rainy Categories:\n{rainy_list}
# Winter Categories:\n{winter_list}

# Query: "{query.strip()}"

# If the query doesn't clearly match anything, return:
# {{ "parent_category": "unknown", "sub_category": "unknown" }}
# """
#     try:
#         response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
#         category_info = response.text.strip()
#         match = re.search(r'\{[\s\S]*?\}', category_info)
#         if match:
#             return json.loads(match.group(0))
#         raise ValueError("No valid JSON returned by Gemini")
#     except Exception as e:
#         print("❌ Gemini category detection error:", e)
#         return {"parent_category": "unknown", "sub_category": "unknown"}
    
#     # # Wrap your call in a simple retry loop with exponential backoff
#     # for attempt in range(3):
#     #     try:
#     #         response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=prompt)
#     #         category_info = response.text.strip()
#     #         match = re.search(r'\{[\s\S]*?\}', category_info)
#     #         if match:
#     #             return json.loads(match.group(0))
            
#     #         # If the model hallucinates non-JSON, we raise a ValueError to trigger the except block
#     #         raise ValueError("No valid JSON returned by Gemini")
            
#     #     except Exception as e:
#     #         print(f"❌ Gemini category detection error (Attempt {attempt + 1}/3):", e)
            
#     #         # Check if the error is due to rate limits or server overload
#     #         if "503" in str(e) or "429" in str(e):
#     #             if attempt < 2: # Don't sleep if it's the very last attempt
#     #                 await asyncio.sleep(2 ** attempt) # Wait 1s, then 2s
#     #                 continue
#     #             else:
#     #                 # If we exhausted all 3 attempts, raise the 503 error for the frontend
#     #                 raise HTTPException(status_code=503, detail="AI_SERVICE_UNAVAILABLE")
            
#     #         # If the error is NOT 503/429 (e.g. prompt issue, bad JSON), return unknown
#     #         return {"parent_category": "unknown", "sub_category": "unknown"}

#     # # Fallback return (should rarely be reached due to the logic above)
#     # return {"parent_category": "unknown", "sub_category": "unknown"}



CATEGORY_MAP = {}
for season, cats in dict1.items():
    for cat in cats:
        CATEGORY_MAP[cat] = season

CATEGORIES_STR = ", ".join(CATEGORY_MAP.keys())

import random
from google import genai
from config import GEMINI_API_KEYS

def get_gemini_client() -> genai.Client:
    api_key = random.choice(GEMINI_API_KEYS)
    print(f"  🔑 Using key: ...{api_key[-6:]}")
    return genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1beta'}
    )

async def detect_query_category(query: str) -> dict:
    
    client = get_gemini_client()

    prompt = f"""You are a product category classifier for an e-commerce platform.

Your job: Given a product search query, find the single best matching category from the list below.

Valid categories (choose ONLY from this list):
{CATEGORIES_STR}

Query: "{query.strip()}"

Rules:
- You MUST return only one category from the valid categories list above
- Do NOT invent or modify category names
- Return JSON only, no explanation, no markdown
- Format: {{"sub_category": "<exact category name from list>"}}
- If nothing matches: {{"sub_category": "unknown"}}"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text.strip()
        match = re.search(r'\{[\s\S]*?\}', text)

        if match:
            result = json.loads(match.group(0))
            sub_cat = result.get("sub_category", "unknown")

            # Derive parent from CATEGORY_MAP
            if sub_cat in CATEGORY_MAP:
                parent_cat = CATEGORY_MAP[sub_cat]

                return {"parent_category": parent_cat, "sub_category": sub_cat}

        return {"parent_category": "unknown", "sub_category": "unknown"}

    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return {"parent_category": "unknown", "sub_category": "unknown"}


async def get_query_embedding_from_category(query: str, CATEGORY_EMBEDDINGS: dict):
    matched_category, _ = match_known_category(query)
    if matched_category and matched_category in CATEGORY_EMBEDDINGS:
        return CATEGORY_EMBEDDINGS[matched_category]["embedding"], matched_category
    # Type 2 — find sub_cat from scraped_products
    from services.mongo_store import get_db
    db = get_db()
    doc = await db.scraped_products.find_one(
        {"query": query}, {"sub_cat": 1, "_id": 0}
    )
    if doc:
        sub_cat = doc.get("sub_cat", "")
        if sub_cat and sub_cat in CATEGORY_EMBEDDINGS:
            return CATEGORY_EMBEDDINGS[sub_cat]["embedding"], sub_cat
    return None, None

async def search_products(
    query: str = Query(..., min_length=1),
    offset: int = Query(0, ge=0),
    limit: int = Query(12, ge=1),
    client_id: str = Query(..., description="Unique ID for the frontend client")
):
    query = query.strip().lower()

    def cyclic_slice(data, offset, limit):
        n = len(data)
        return [data[(offset + i) % n] for i in range(limit)]

    matched_category, parent_folder = match_known_category(query)

    if matched_category:
        if not parent_folder:
            raise HTTPException(status_code=404, detail="Matching folder not found.")
        season = parent_folder.replace("_categories", "")
        data = await get_products_by_season_category(season, matched_category)
        if not data:
            raise HTTPException(status_code=404, detail="Product file not found.")
        random.shuffle(data)
        return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

    else:
        already_scraped = await is_query_scraped(query)

        if already_scraped:
            data = await get_scraped_products(query)
            if not data:
                raise HTTPException(status_code=404, detail="No scraped products found.")
            random.shuffle(data)
            return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

        try:
            category_info = await detect_query_category(query)
            parent_cat = category_info.get("parent_category", "unknown")
            sub_cat    = category_info.get("sub_category", "unknown")

            # Add this trap right here
            if parent_cat == "unknown" or sub_cat == "unknown":
                raise HTTPException(status_code=400, detail="CATEGORY_UNKNOWN")
            
            if parent_cat != "unknown" and sub_cat != "unknown":
                category_details = seasonal_categories.get(parent_cat, {}).get(sub_cat)

                if category_details:
                    if query in _in_flight_scrapes:
                        await ws_manager.send_personal_message("[SYSTEM] ⏳ Identical query in progress. Linking to stream...", client_id)
                        await _in_flight_scrapes[query].wait() 
                    else:
                        current_scrape_event = asyncio.Event()
                        _in_flight_scrapes[query] = current_scrape_event

                        try:
                            if _scraper_semaphore.locked():
                                await ws_manager.send_personal_message("[SYSTEM] ⏳ System busy processing another request. You are in the queue...", client_id)

                            async with _scraper_semaphore:
                                await ws_manager.send_personal_message("[SYSTEM] 🟢 Slot acquired! Routing to local worker...", client_id)
                                
                                if not ACTIVE_WORKER_URL:
                                    raise HTTPException(status_code=503, detail="WORKER_OFFLINE")

                                payload = {
                                    "query": query,
                                    "category_name": sub_cat,
                                    "selector_type": category_details["selector_type"],
                                    "selector_value": category_details["selector_value"],
                                    "client_id": client_id,
                                    "max_items": 5,
                                    "render_url": os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
                                }

                                try:
                                    async with httpx.AsyncClient(timeout=180.0) as client_http:
                                        response = await client_http.post(f"{ACTIVE_WORKER_URL}/api/worker/scrape", json=payload)
                                        
                                        if response.status_code != 200:
                                            # Trap 2: Ngrok is up, but worker crashed
                                            raise HTTPException(status_code=503, detail="WORKER_OFFLINE")

                                        scraped = response.json().get("data", [])

                                except (httpx.RequestError, httpx.TimeoutException):
                                    # Trap 3: Ngrok is entirely turned off/unreachable
                                    raise HTTPException(status_code=503, detail="WORKER_OFFLINE")
                                
                                await set_scraped_products(query, parent_cat, sub_cat, scraped)
                                
                                await ws_manager.send_personal_message("[SYSTEM] ⏱ Extraction complete. Cooling down network connections (5s)...", client_id)
                                await asyncio.sleep(5)

                        except HTTPException:
                            # CRITICAL: Let our custom 503 error pass through to the frontend
                            raise
                        
                        except Exception as e:
                            await ws_manager.send_personal_message(f"[ERROR] ❌ Cloud worker connection failed.", client_id)
                            raise HTTPException(status_code=500, detail="Worker failed")

                        finally:
                            _in_flight_scrapes.pop(query, None)
                            current_scrape_event.set()

                    data = await get_scraped_products(query)
                    if not data:
                        raise HTTPException(status_code=404, detail="No scraped products found.")
                    random.shuffle(data)
                    return [NewProduct(**item) for item in cyclic_slice(data, offset, limit)]

        except HTTPException:
            raise
        except Exception as e:
            print(f"Scraping error: {e}")

    raise HTTPException(status_code=404, detail="No results found.")