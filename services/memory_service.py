# # services/memory_service.py

# # Decaying of memory based on session date

# import json, math, os
# import numpy as np
# from datetime import datetime
# from  config import (
#     PAST_EMBEDDING_FILE,
#     SESSION_META_FILE,
#     LAMBDA,
#     EMBEDDING_SIZE,
#     USER_INTEREST_FILE
# )
# from services.recommendation_service import search_similar_items

# def today_str():
#     return datetime.now().date().isoformat()

# def get_past_embedding():
#     if os.path.exists(PAST_EMBEDDING_FILE):
#         return json.load(open(PAST_EMBEDDING_FILE))
#     return [0.0]*EMBEDDING_SIZE

# def get_last_session_date():
#     if not os.path.exists(SESSION_META_FILE):
#         return None

#     with open(SESSION_META_FILE, "r", encoding="utf-8") as f:
#         try:
#             return json.load(f).get("last_session_date")
#         except:
#             return None
        
# def update_session_date():
#     with open(SESSION_META_FILE, "w", encoding="utf-8") as f:
#         json.dump(
#             {"last_session_date": today_str()},
#             f,
#             indent=2
#         )


# def apply_time_decay_to_past_embedding_using_session_date():
#     if not os.path.exists(PAST_EMBEDDING_FILE):
#         return

#     # Load past embedding
#     with open(PAST_EMBEDDING_FILE, "r", encoding="utf-8") as f:
#         past_embedding = np.array(json.load(f))

#     # Load last session date
#     if not os.path.exists(SESSION_META_FILE):
#         return

#     with open(SESSION_META_FILE, "r", encoding="utf-8") as f:
#         last_session_date_str = json.load(f).get("last_session_date")

#     if not last_session_date_str:
#         return

#     last_session_date = datetime.fromisoformat(last_session_date_str).date()
#     today = datetime.now().date()

#     delta_days = (today - last_session_date).days

#     if delta_days <= 0:
#         return  # same day → no decay

#     decay_factor = math.exp(-LAMBDA * delta_days)
#     decay_factor = max(0.05, decay_factor)  # keep memory essence

#     decayed_embedding = (past_embedding * decay_factor).tolist()

#     # Save back
#     with open(PAST_EMBEDDING_FILE, "w", encoding="utf-8") as f:
#         json.dump(decayed_embedding, f)

#     print(
#         f"🧠 Decay applied using session date | "
#         f"days_gap={delta_days} | factor={decay_factor:.4f}"
#     )



# def initialize_session_if_needed():
#     last_session_date = get_last_session_date()
#     if(last_session_date is None):
#         print("🟡 No session date found → initializing")
#         update_session_date()
#         return
    
#     today = today_str()

#     if last_session_date == today:
#         print("🟢 Same day → no decay")
#         return

#     print("🧠 New day → applying decay & regenerating AI picks")

#     # ✅ decay using session date ONLY
#     apply_time_decay_to_past_embedding_using_session_date()

#     # regenerate user_interest.json
#     past_embedding = get_past_embedding()
#     recommendations = search_similar_items(past_embedding)

#     with open(USER_INTEREST_FILE, "w", encoding="utf-8") as f:
#         json.dump(recommendations, f, indent=2, ensure_ascii=False)

#     update_session_date()





# # mongodb for single user handling 
# # services/memory_service.py

# import math, numpy as np
# from datetime import datetime
# from config import LAMBDA, EMBEDDING_SIZE

# def today_str():
#     return datetime.now().date().isoformat()

# async def get_past_embedding():
#     from services.mongo_store import get_past_user_embedding
#     result = await get_past_user_embedding()
#     return result if result else [0.0] * EMBEDDING_SIZE

# async def get_last_session_date():
#     from services.mongo_store import get_session_meta
#     meta = await get_session_meta()
#     return meta.get("last_session_date")

# async def update_session_date():
#     from services.mongo_store import set_session_meta
#     await set_session_meta({"last_session_date": today_str()})

# async def apply_time_decay():
#     from services.mongo_store import get_past_user_embedding, set_past_user_embedding, get_session_meta
#     doc = await get_past_user_embedding()
#     if not doc:
#         return
#     past_embedding = np.array(doc)
#     meta = await get_session_meta()
#     last_date_str = meta.get("last_session_date")
#     if not last_date_str:
#         return
#     last_date = datetime.fromisoformat(last_date_str).date()
#     today = datetime.now().date()
#     delta_days = (today - last_date).days
#     if delta_days <= 0:
#         return
#     decay_factor = max(0.05, math.exp(-LAMBDA * delta_days))
#     decayed = (past_embedding * decay_factor).tolist()
#     await set_past_user_embedding(decayed)
#     print(f"🧠 Decay applied | days={delta_days} | factor={decay_factor:.4f}")

# async def initialize_session_if_needed():
#     from services.mongo_store import set_user_interest
#     from services.recommendation_service import search_similar_items

#     last_date = await get_last_session_date()
#     if last_date is None:
#         print("🟡 No session date → initializing")
#         await update_session_date()
#         return

#     today = today_str()
#     if last_date == today:
#         print("🟢 Same day → no decay")
#         return

#     print("🧠 New day → applying decay & regenerating AI picks")
#     await apply_time_decay()
#     past_emb = await get_past_embedding()
#     recommendations = search_similar_items(past_emb)
#     await set_user_interest(recommendations)
#     await update_session_date()




# mongodb for multi user handling 
# services/memory_service.py

import math, numpy as np
from datetime import datetime
from config import LAMBDA, EMBEDDING_SIZE

def today_str():
    return datetime.now().date().isoformat()

async def get_past_embedding(user_id: str):
    from services.mongo_store import get_past_user_embedding
    result = await get_past_user_embedding(user_id)
    return result if result else [0.0] * EMBEDDING_SIZE

async def get_last_session_date(user_id: str):
    from services.mongo_store import get_session_meta
    meta = await get_session_meta(user_id)
    return meta.get("last_session_date")

async def update_session_date(user_id: str):
    from services.mongo_store import set_session_meta
    await set_session_meta(user_id, {"last_session_date": today_str()})

async def apply_time_decay(user_id: str):
    from services.mongo_store import get_past_user_embedding, set_past_user_embedding, get_session_meta
    doc = await get_past_user_embedding(user_id)
    if not doc:
        return
    past_embedding = np.array(doc)
    meta = await get_session_meta(user_id)
    last_date_str = meta.get("last_session_date")
    if not last_date_str:
        return
    last_date = datetime.fromisoformat(last_date_str).date()
    today = datetime.now().date()
    delta_days = (today - last_date).days
    if delta_days <= 0:
        return
    decay_factor = max(0.05, math.exp(-LAMBDA * delta_days))
    decayed = (past_embedding * decay_factor).tolist()
    await set_past_user_embedding(user_id, decayed)
    print(f"🧠 Decay applied | days={delta_days} | factor={decay_factor:.4f}")

async def initialize_session_if_needed(user_id: str):
    from services.mongo_store import set_user_interest
    from services.recommendation_service import search_similar_items

    last_date = await get_last_session_date(user_id)
    if last_date is None:
        print("🟡 No session date → initializing")
        await update_session_date(user_id)
        return

    today = today_str()
    if last_date == today:
        print("🟢 Same day → no decay")
        return

    print("🧠 New day → applying decay & regenerating AI picks")
    await apply_time_decay(user_id)
    past_emb = await get_past_embedding(user_id)
    recommendations = search_similar_items(past_emb)
    await set_user_interest(user_id, recommendations)
    await update_session_date(user_id)