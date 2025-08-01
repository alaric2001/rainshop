from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Any
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter(prefix="/sales", tags=["Sales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item(frm: schemas.sales.SalesForm, db: Session = Depends(get_db)):
    return crud.sales.create_sales(db, frm)

@router.post("/debug")
async def receive_any_json(payload: Any = Body(...)):
    print("Received payload:", payload)  # Debug log
    return {"received": payload}

