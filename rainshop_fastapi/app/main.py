from fastapi import FastAPI
from app.routers.itembarang import router as item_router
from app.routers.item_images import router as image_router
from app.database import Base, engine
# from app.models import ItemBarang, ItemImage  # penting: agar model terdaftar
from fastapi.middleware.cors import CORSMiddleware  # <-- Tambahkan ini

from pydantic import BaseModel #printer
from typing import List
from app.printers.bluetooth import print_receipt

from app.routers.print import router as print_router #printer Alternatif Tanpa pybluez

Base.metadata.create_all(bind=engine)

app = FastAPI()

class PrintItem(BaseModel): #printer
    name: str
    qty: int
    price: int

class PrintRequest(BaseModel):
    bt_address: str
    items: List[PrintItem]

# Izinkan CORS untuk semua origin (*) atau spesifik ke Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan origin Vue.js
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua method (GET, POST, dll.)
    allow_headers=["*"],  # Izinkan semua header
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine) # Membuat tabel jika belum ada



app.include_router(item_router)
app.include_router(image_router)
app.include_router(print_router) #printer Alternatif Tanpa pybluez

@app.post("/print")
async def print_struk(data: PrintRequest):
    total = sum([item.qty * item.price for item in data.items])
    result = print_receipt(data.bt_address, data.items, total)
    return result

# --- Endpoint Utama ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to Rainshop fastAPI with SQLAlchemy!"}