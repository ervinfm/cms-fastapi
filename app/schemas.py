from pydantic import BaseModel, EmailStr, Field
from enum import Enum

# Skema untuk Role User
class UserRole(str, Enum):
    admin = "admin"
    user = "user"

# Skema untuk register user
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern="^[a-zA-Z0-9_.-]+$")
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

# Skema untuk membaca user (tanpa password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    
    class Config:
        from_attributes = True

# Skema untuk autentikasi login
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# Skema untuk membuat konten
class ContentCreate(BaseModel):
    title: str
    body: str

# Skema untuk membaca konten
class ContentResponse(ContentCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

