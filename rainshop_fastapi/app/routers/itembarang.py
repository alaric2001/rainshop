from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter(prefix="/items", tags=["ItemBarang"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/search", response_model=List[schemas.vw_itembarang.VwItemBarangOut])
def search_items(payload: schemas.itembarang.ImageSearchRequest, db: Session = Depends(get_db)):
    # print("✅ Menerima image:", payload.image)
    return crud.itembarang.search_items(db, payload.image)

@router.post("/")
def create_item(item: schemas.itembarang.ItemBarangCreate, db: Session = Depends(get_db)):
    return crud.itembarang.create_item(db, item)


@router.get("/", response_model=List[schemas.itembarang.ItemBarangOut])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.itembarang.get_all_items(db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=schemas.itembarang.ItemBarangOut)
def read_item(item_id: str, db: Session = Depends(get_db)):
    db_item = crud.itembarang.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
