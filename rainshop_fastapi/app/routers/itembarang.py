from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Any
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

# @router.post("/")
# async def receive_any_json(payload: Any = Body(...)):
#     print("Received payload:", payload)  # Debug log
#     return {"received": payload}


@router.put("/{item_id}")
def update_item(item_id: str, frm: schemas.itembarang.ItemBarangUpdate, db: Session = Depends(get_db)):
    return crud.itembarang.update_item(db, item_id, frm)

@router.get("/", response_model=schemas.itembarang.PaginatedResponse[schemas.itembarang.ItemBarangOut])
def read_items(item_name: str = "", page: int = 1, limit: int = 10, sortBy: str = "item_name", sortDir: str = "asc", item_stock: int = None, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    items, total = crud.itembarang.get_all_items(db, item_name, skip=skip, limit=limit, sortBy=sortBy, sortDir=sortDir, item_stock=item_stock)
    
    return {
        "data": items,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/{item_id}", response_model=schemas.itembarang.ItemBarangOut)
def read_item(item_id: str, db: Session = Depends(get_db)):
    db_item = crud.itembarang.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
