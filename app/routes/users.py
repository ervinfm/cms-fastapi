from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.utils.security import get_current_user,  hash_password, get_admin_user
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

limiter = Limiter(key_func=get_remote_address)

# Almbil semua Data user untuk admin
@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_admin_user)):
    users = db.query(models.User).all()
    return users

# Ambil detail user
@router.get("/{user_id}", response_model=schemas.UserResponse)
@limiter.limit("10/minute")  # Maksimal 10 request per menit
def get_user(request: Request, user_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user
@router.put("/{user_id}", response_model=schemas.UserResponse)
@limiter.limit("5/minute")  # Maksimal 5 request per menit
def update_user(request: Request, user_id: int, user_data: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = user_data.username
    user.email = user_data.email
    user.password = hash_password(user_data.password) 

    db.commit()
    db.refresh(user)
    return user

# Hapus user
@router.delete("/{user_id}")
@limiter.limit("3/minute")  # Maksimal 3 request per menit
def delete_user(request: Request, user_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logging.error(f"Attempted to delete non-existing user with ID {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logging.info(f"User {user.username} (ID: {user_id}) deleted successfully")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
