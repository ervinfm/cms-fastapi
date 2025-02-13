from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import database, models
from dotenv import load_dotenv
from jose import jwt, JWTError
import os
import re

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = verify_access_token(token)
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def get_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    user = get_current_user(token, db)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access this resource")
    return user

def validate_password(password: str):
    """
    Memeriksa apakah password memenuhi syarat keamanan:
    - Minimal 8 karakter
    - Mengandung huruf besar dan kecil
    - Mengandung angka
    - Mengandung karakter spesial
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password harus minimal 8 karakter.")
    
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password harus mengandung setidaknya satu huruf besar.")

    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password harus mengandung setidaknya satu huruf kecil.")

    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password harus mengandung setidaknya satu angka.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password harus mengandung setidaknya satu karakter spesial.")
    
    return password