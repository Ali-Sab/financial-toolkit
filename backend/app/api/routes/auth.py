from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db  # your DB session dependency
from app.db.models import User
from app.schemas import UserCreate, UserLogin, TokenData, RefreshToken
from app.utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user, create_refresh_token, validate_refresh_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Register
@router.post("/auth/register", response_model=TokenData)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
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
    return {"access_token": access_token, "refresh_token": refresh_token}

# Login
@router.post("/auth/token", response_model=TokenData)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.email == user_data.email))
    user = user.scalar_one_or_none()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token({"sub": str(user.id)}, db)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/auth/refresh", response_model=TokenData)
async def refresh_token(refresh_token_input: RefreshToken, db: AsyncSession = Depends(get_db)):
    user_id = await validate_refresh_token(refresh_token_input.refresh_token, db)
    access_token = create_access_token({"sub": user_id})
    refresh_token = await create_refresh_token({"sub": user_id}, db)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "username": current_user.username, "id": current_user.id}
