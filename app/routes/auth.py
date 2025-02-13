from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from dotenv import load_dotenv

from app import models, schemas, database
from app.utils.security import hash_password, verify_password, validate_password

from slowapi import Limiter
from slowapi.util import get_remote_address

import os
import logging

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

# Fungsi untuk membuat JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint register user
@router.post("/register", response_model=schemas.UserResponse)
@limiter.limit("3/minute")  # Maksimal 3 registrasi per menit
def register(request: Request, user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Cek apakah email sudah digunakan
    existing_email = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar.")
    
    # Cek apakah username sudah digunakan
    existing_username = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username sudah digunakan.")
    
    # Validasi password sebelum di-hash
    validate_password(user_data.password)

    hashed_password = hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role  # Default user biasa
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Endpoint login user
@router.post("/token", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: schemas.LoginSchema, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.password):
        logging.warning(f"Failed login attempt for email: {form_data.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    logging.info(f"User {user.username} logged in successfully")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
