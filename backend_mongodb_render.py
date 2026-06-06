import sys, random, os
from fastapi import FastAPI, HTTPException, Query, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import numpy as np
import asyncio

# Local Imports
from config import *
from models.schema import NewProduct, UserBehavior
from domain.categories import dict1, dict2
from db import connect_db, close_db
from auth import get_current_user, verify_google_token, get_or_create_user, create_jwt

# Services
from services.mongo_store import (
    get_all_category_embeddings, upsert_similarity_scores,
    get_display_products, get_popular_products, set_popular_products,
    append_behavior_log, get_behavior_log,
    get_user_interest, set_user_interest,
    get_products_by_season_category, get_category_similarity_scores,
    get_products_by_season
)
from services.recommendation_service import (
    get_query_embedding, compute_weight,
    get_past_embedding, save_past_embedding,
    search_similar_items, update_user_embedding
)
from services.memory_service import initialize_session_if_needed
from services.ws_manager import ws_manager

import services.search_service as search_service
from services.search_service import search_products


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CATEGORY_EMBEDDINGS = {}

@app.on_event("startup")
async def startup():
    global CATEGORY_EMBEDDINGS
    await connect_db()
    CATEGORY_EMBEDDINGS = await get_all_category_embeddings()
    print(f"✅ Loaded {len(CATEGORY_EMBEDDINGS)} category embeddings from MongoDB")

@app.on_event("shutdown")
async def shutdown():
    await close_db()


# ── helpers ───────────────────────────────────────────────────────────────────

def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def get_category_folder(category_name):
    for group_name, categories in dict1.items():
        if category_name in categories:
            return group_name
    return None

def get_current_season() -> str:
    month = datetime.now().month
    if month in [3, 4, 5, 6]: return "summer"
    elif month in [7, 8, 9]: return "rainy"
    else: return "winter"

async def get_top_similar_categories(user_id: str, overall_embedding, top_k=5):
    category_scores = []
    for category_name, category_data in CATEGORY_EMBEDDINGS.items():
        similarity = cosine_similarity(overall_embedding, category_data["embedding"])
        category_scores.append({
            "category": category_name,
            "score": float(similarity),
            "image_url": category_data["image_url"]
        })
    category_scores.sort(key=lambda x: x["score"], reverse=True)
    await upsert_similarity_scores(user_id, category_scores)
    return category_scores[:top_k]


# ── auth endpoints ────────────────────────────────────────────────────────────

class GoogleAuthRequest(BaseModel):
    token: str

@app.post("/auth/google")
async def google_auth(body: GoogleAuthRequest):
    google_info = await verify_google_token(body.token)
    user = await get_or_create_user(google_info)
    jwt_token = create_jwt(
        user_id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        picture=user["picture"]
    )
    return {
        "token": jwt_token,
        "user": {
            "email": user["email"],
            "name": user["name"],
            "picture": user["picture"]
        }
    }

@app.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["sub"],
        "email": current_user["email"],
        "name": current_user["name"],
        "picture": current_user["picture"]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}


# ── core data endpoints ───────────────────────────────────────────────────────

@app.get("/api/user-signals")
async def get_user_signals(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["sub"]
        logs = await get_behavior_log(user_id)
        formatted = [{
            "query": item.get("query", ""),
            "time_spent": item.get("timeSpent", 0),
            "click_count": item.get("clickCount", 0),
            "scroll_depth": item.get("scrollDepth", 0),
            "timestamp": item.get("timestamp", "")
        } for item in logs]
        return {"signals": formatted}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load user signals")


@app.get("/api/ai-recommendations", response_model=List[NewProduct])
async def get_ai_recommendations(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["sub"]
        await initialize_session_if_needed(user_id)
        data = await get_user_interest(user_id)
        if data:
            print("✅ Loaded user_interest from MongoDB")
            return [NewProduct(**item) for item in data]
        print("⚠️ user_interest empty → falling back to display")
        data = await get_display_products()
        return [NewProduct(**item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products", response_model=List[NewProduct])
async def get_products(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["sub"]
        data = await get_popular_products(user_id)
        if not data:
            data = await get_display_products()
        products = [NewProduct(**item) for item in data]
        random.shuffle(products)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/you-might-like", response_model=List[NewProduct])
async def get_you_might_like():
    try:
        current_season = get_current_season()
        seasonal_data = await get_products_by_season(current_season)
        evergreen_data = await get_products_by_season("evergreen")
        seasonal_sample = random.sample(seasonal_data, min(30, len(seasonal_data)))
        evergreen_sample = random.sample(evergreen_data, min(10, len(evergreen_data)))
        combined = seasonal_sample + evergreen_sample
        random.shuffle(combined)
        return [NewProduct(**item) for item in combined]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load You Might Like")

@app.get("/api/category-insights")
async def get_category_insights(current_user: dict = Depends(get_current_user)):
    user_id = current_user["sub"]
    data = await get_category_similarity_scores(user_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Similarity scores not yet computed. Trigger a recommendation cycle first."
        )
    return JSONResponse(content=data)


# ── deployment architecture (websockets & ngrok routing) ──────────────────────

class WorkerUrlPayload(BaseModel):
    url: str

class LogPayload(BaseModel):
    client_id: str
    message: str
    level: str = "SYSTEM"

@app.websocket("/ws/search/{client_id}")
async def websocket_terminal_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Pass the specific websocket to prevent deleting concurrent reconnections
        ws_manager.disconnect(client_id, websocket)

@app.post("/api/admin/set-worker")
async def set_worker_url(payload: WorkerUrlPayload):
    """
    Dynamically routes Render's backend to your active local ngrok tunnel.
    """
    clean_url = payload.url.strip().rstrip("/")
    if not clean_url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL format.")
        
    search_service.ACTIVE_WORKER_URL = clean_url
    print(f"Ngrok worker URL updated: {clean_url}")
    return {"status": "success", "active_worker_url": search_service.ACTIVE_WORKER_URL}

@app.post("/api/internal/log")
async def receive_worker_log(payload: LogPayload):
    """
    Receives logs from the local laptop Playwright scraper and bridges 
    them to the React frontend user via WebSockets.
    """
    # The clean visual format handled by React expects raw strings mostly, 
    # but we can pass the level tag along for coloring
    formatted_message = f"[{payload.level}] {payload.message}"
    await ws_manager.send_personal_message(formatted_message, payload.client_id)
    return {"status": "delivered"}

@app.get("/api/search", response_model=List[NewProduct])
async def search_api(
    query: str = Query(..., min_length=1),
    offset: int = Query(0, ge=0),
    limit: int = Query(12, ge=1),
    client_id: str = Query(..., description="Unique ID for the frontend client")
):
    results = await search_products(query, offset, limit, client_id=client_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results


# ── user tracking & embeddings ────────────────────────────────────────────────

@app.post("/api/track_user_behavior")
async def track_user_behavior(
    data: UserBehavior,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["sub"]

    log_entry = {
        "query": data.query,
        "timeSpent": data.timeSpent,
        "scrollDepth": data.scrollDepth,
        "clickCount": data.clickCount,
        "timestamp": datetime.now().isoformat()
    }
    await append_behavior_log(user_id, log_entry)

    # use category embedding instead of sentence transformer
    query_embedding = await get_query_embedding(data.query, CATEGORY_EMBEDDINGS)
    past_embedding = await get_past_embedding(user_id)
    weight = compute_weight(data.timeSpent, data.clickCount, data.scrollDepth)
    overall_embedding = update_user_embedding(query_embedding, past_embedding, weight)
    await save_past_embedding(user_id, overall_embedding)

    try:
        top_category_objects = await get_top_similar_categories(user_id, overall_embedding, top_k=5)
        top_categories = [item["category"] for item in top_category_objects]

        current_season = get_current_season()
        seasonal_key = f"{current_season}_categories"
        seasonal_cats = dict1.get(seasonal_key, [])
        seasonal_cats = random.sample(seasonal_cats, min(5, len(seasonal_cats)))

        final_categories = list(dict.fromkeys(top_categories + seasonal_cats))
        print("\nPopular Product Categories:", final_categories)

        count = 0
        popular_products = []
        for category_name in final_categories:
            count = count + 1
            folder_name = get_category_folder(category_name)
            if not folder_name:
                continue
            season = folder_name.replace("_categories", "")
            products = await get_products_by_season_category(season, category_name)
            if count > 5:
                number_products = 2
            else:
                number_products = 5
            popular_products.extend(products[:number_products])

        await set_popular_products(user_id, popular_products)
        print(f"\nPopular products updated: {len(popular_products)} items")

    except Exception as e:
        print("Popular products generation failed:", str(e))

    recommendations = search_similar_items(overall_embedding)
    await set_user_interest(user_id, recommendations)

    return {
        "status": "success",
        "message": "User behavior logged, embedding updated, and recommendations saved.",
        "recommendations_count": len(recommendations)
    }