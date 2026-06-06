# auth.py

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from config import GOOGLE_CLIENT_ID, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from db import get_db

security = HTTPBearer()

def create_jwt(user_id: str, email: str, name: str, picture: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "picture": picture,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    return verify_jwt(credentials.credentials)

async def verify_google_token(token: str) -> dict:
    try:
        info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        return info
    except Exception as e:
        print(f"❌ Google token error: {e}")
        raise HTTPException(status_code=401, detail="Invalid Google token")

async def get_or_create_user(google_info: dict) -> dict:
    db = get_db()
    google_id = google_info["sub"]
    user = await db.users.find_one({"google_id": google_id})
    if not user:
        user = {
            "google_id": google_id,
            "email": google_info["email"],
            "name": google_info.get("name", ""),
            "picture": google_info.get("picture", ""),
            "created_at": datetime.utcnow().isoformat()
        }
        result = await db.users.insert_one(user)
        user["_id"] = str(result.inserted_id)
    else:
        user["_id"] = str(user["_id"])
    return user