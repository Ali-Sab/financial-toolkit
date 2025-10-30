from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User
from app.schemas import UserCreate

class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, user_data: UserCreate, password_hash: str) -> User:
        user = User(email=user_data.email, username=user_data.username, password_hash=password_hash)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

user_repository = UserRepository()
