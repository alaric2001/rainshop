from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter(prefix="/images", tags=["ItemImages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.item_images.ItemImageOut)
def create_image(image: schemas.item_images.ItemImageCreate, db: Session = Depends(get_db)):
    return crud.item_images.create_image(db, image)

@router.get("/by-item/{item_id}", response_model=List[schemas.item_images.ItemImageOut])
def get_images_by_item(item_id: str, db: Session = Depends(get_db)):
    return crud.item_images.get_images_by_item_id(db, item_id)
