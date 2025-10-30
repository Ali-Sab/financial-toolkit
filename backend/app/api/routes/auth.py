from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.db.models import User
from app.schemas import UserCreate, UserLogin
from app.utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user, create_refresh_token, validate_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from app.repositories.user_repository import user_repository

router = APIRouter()

def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/auth/register")
async def register(user_data: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    if await user_repository.get_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user_data.password)
    new_user = await user_repository.create(db, user_data, hashed_pw)

    access_token = create_access_token({"sub": str(new_user.id)})
    refresh_token = await create_refresh_token({"sub": str(new_user.id)}, db)
    set_auth_cookies(response, access_token, refresh_token)
    return {"message": "Registration successful"}

@router.post("/auth/login")
async def login(user_data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token({"sub": str(user.id)}, db)
    set_auth_cookies(response, access_token, refresh_token)
    return {"message": "Login successful"}

@router.post("/auth/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(None), db: AsyncSession = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    user_id = await validate_refresh_token(refresh_token, db)
    access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = await create_refresh_token({"sub": str(user_id)}, db)
    set_auth_cookies(response, access_token, new_refresh_token)
    return {"message": "Token refreshed"}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

@router.get("/auth/session")
async def get_session(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "username": current_user.username}
