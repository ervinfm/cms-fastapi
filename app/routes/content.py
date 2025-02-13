from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.utils.security import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(
    prefix="/content",
    tags=["Content"]
)

limiter = Limiter(key_func=get_remote_address)

# Ambil semua konten user
@router.get("/", response_model=list[schemas.ContentResponse])
@limiter.limit("20/minute")  # Maksimal 20 request per menit
def get_all_content(request: Request, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    content = db.query(models.Content).filter(models.Content.owner_id == current_user.id).all()
    return content

# Tambah konten baru
@router.post("/", response_model=schemas.ContentResponse)
@limiter.limit("5/minute")  # Maksimal 5 konten baru per menit
def create_content(request: Request, content_data: schemas.ContentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_content = models.Content(title=content_data.title, body=content_data.body, owner_id=current_user.id)
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content

# Ambil detail konten
@router.get("/{content_id}", response_model=schemas.ContentResponse)
@limiter.limit("15/minute")  # Maksimal 15 request per menit
def get_content(request: Request, content_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    content = db.query(models.Content).filter(models.Content.id == content_id, models.Content.owner_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

# Update konten
@router.put("/{content_id}", response_model=schemas.ContentResponse)
@limiter.limit("5/minute")  # Maksimal 5 update per menit
def update_content(request: Request, content_id: int, content_data: schemas.ContentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    content = db.query(models.Content).filter(models.Content.id == content_id, models.Content.owner_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    content.title = content_data.title
    content.body = content_data.body

    db.commit()
    db.refresh(content)
    return content

# Hapus konten
@router.delete("/{content_id}")
@limiter.limit("3/minute")  # Maksimal 3 request per menit
def delete_content(request: Request, content_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    content = db.query(models.Content).filter(models.Content.id == content_id, models.Content.owner_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    db.delete(content)
    db.commit()
    return {"message": "Content deleted successfully"}
