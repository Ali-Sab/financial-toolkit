from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.db.models import User
from app.schemas import UserCreate, UserLogin
from app.utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user, create_refresh_token, validate_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Register
@router.post("/auth/register")
async def register(user_data: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.email == user_data.email))
    if user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user_data.password)
    new_user = User(email=user_data.email, username=user_data.username, password_hash=hashed_pw)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token({"sub": str(new_user.id)})
    refresh_token = await create_refresh_token({"sub": str(new_user.id)}, db)
    
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
    
    return {"message": "Registration successful"}

# Login
@router.post("/auth/login")
async def login(user_data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.email == user_data.email))
    user = user.scalar_one_or_none()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token({"sub": str(user.id)}, db)
    
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
    
    return {"message": "Login successful"}

@router.post("/auth/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(None), db: AsyncSession = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    user_id = await validate_refresh_token(refresh_token, db)
    access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = await create_refresh_token({"sub": str(user_id)}, db)
    
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
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return {"message": "Token refreshed"}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "username": current_user.username, "id": current_user.id}
