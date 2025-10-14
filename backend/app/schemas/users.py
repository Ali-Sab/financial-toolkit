from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
