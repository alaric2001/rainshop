from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List, Any
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter(prefix="/images", tags=["ItemImages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_image(frm: schemas.item_images.ItemImageForm, db: Session = Depends(get_db)):
    return crud.item_images.create_image(db, frm)

@router.post("/search", response_model=List[schemas.vw_itembarang.VwItemBarangOut])
def search_image(payload: schemas.itembarang.ImageSearchRequest, db: Session = Depends(get_db)):
    return crud.item_images.search_image(db, payload.image)


@router.put("/{image_id}")
def update_image(image_id: str, frm: schemas.item_images.ItemImageUpdate, db: Session = Depends(get_db)):
    return crud.item_images.update_image(db, image_id, frm.image)

# @router.put("/{image_id}")
# async def receive_any_json(image_id: str,payload: Any = Body(...)):
#     print("✅ Menerima image:", image_id)
#     print("Received payload:", payload)  # Debug log
#     return {"received": payload}


@router.get("/{image_id}")
def get_image(image_id: str, db: Session = Depends(get_db)):
    return crud.item_images.get_image(db, image_id)

@router.get("/by-item/{item_id}", response_model=List[schemas.item_images.ItemImageOut])
def get_images_by_item(item_id: str, db: Session = Depends(get_db)):
    return crud.item_images.get_images_by_item_id(db, item_id)
