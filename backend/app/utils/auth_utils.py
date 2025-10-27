import os
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db import User, get_db, RefreshToken
from dotenv import load_dotenv
import traceback


# Load environment variables from .env
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(data: dict, db: AsyncSession):
    user_id = int(data['sub'])
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "refresh"})

    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token_db = RefreshToken(refresh_token=refresh_token, user_id=user_id, expires_at=expire)

    await db.execute(delete(RefreshToken).where(RefreshToken.user_id == user_id))
    
    db.add(refresh_token_db)
    await db.commit()
    await db.refresh(refresh_token_db)
    
    return refresh_token

async def validate_refresh_token(refresh_token_str: str, db: AsyncSession):
    refresh_token = await db.execute(select(RefreshToken).where(RefreshToken.refresh_token == refresh_token_str))
    refresh_token = refresh_token.scalar_one_or_none()
    if not refresh_token or refresh_token.expires_at < datetime.now(timezone.utc) or refresh_token.revoked is True:
        if refresh_token:
            db.delete(refresh_token)
            await db.commit()
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return refresh_token.user_id

async def get_current_user(
    access_token: str = Cookie(None), db: AsyncSession = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as err:
        print(err)
        traceback.format_exc()
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(user_id)
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
