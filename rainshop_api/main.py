# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import List # <--- TAMBAHKAN BARIS INI

# Impor dari file lokal yang baru kita buat
from . import models, schemas
from .database import engine, get_db, Base

app = FastAPI()

# --- Fungsi untuk Membuat Tabel di Database ---
# Anda bisa panggil ini sekali saat aplikasi pertama kali dijalankan
# atau secara manual di awal pengembangan.
# Untuk produksi, Anda mungkin menggunakan migrasi database (misalnya Alembic).
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine) # Membuat tabel jika belum ada

# --- Endpoint untuk Menguji Koneksi Database (Opsional) ---
@app.get("/db-status")
async def get_db_status(db: Session = Depends(get_db)):
    """
    Endpoint untuk memeriksa status koneksi database.
    """
    try:
        # Lakukan query sederhana untuk memastikan koneksi berfungsi
        db.execute(models.ItemBarang.__table__.select().limit(1))
        return {"status": "Database connection successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {e}"
        )

# --- Endpoint untuk Membuat Produk Baru ---
@app.post("/products/", response_model=schemas.ItemBarang, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ItemBarangCreate, db: Session = Depends(get_db)):
    """
    Menambahkan produk baru ke database. item_id akan digenerate otomatis sebagai UUID.
    """
    db_product = models.ItemBarang(
        item_id=str(uuid.uuid4()), # Generate UUID baru
        item_name=product.item_name,
        item_price=product.item_price,
        isactive=product.isactive
    )
    db.add(db_product) # Tambahkan objek ke sesi
    db.commit() # Simpan perubahan ke database
    db.refresh(db_product) # Perbarui objek dengan data dari DB (misal default values)
    return db_product

# --- Endpoint untuk Mendapatkan Semua Produk ---
@app.get("/products/", response_model=List[schemas.ItemBarang]) # Baris ini yang menyebabkan error
async def get_all_products(db: Session = Depends(get_db)):
    """
    Mendapatkan daftar semua produk dari database.
    """
    products = db.query(models.ItemBarang).all() # Mengambil semua item
    return products

# --- Endpoint untuk Mendapatkan Produk Berdasarkan ID ---
@app.get("/products/{item_id}", response_model=schemas.ItemBarang)
async def get_product_by_id(item_id: str, db: Session = Depends(get_db)):
    """
    Mendapatkan detail produk berdasarkan ID (UUID).
    """
    product = db.query(models.ItemBarang).filter(models.ItemBarang.item_id == item_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# --- Endpoint untuk Memperbarui Produk ---
@app.put("/products/{item_id}", response_model=schemas.ItemBarang)
async def update_product(item_id: str, product_update: schemas.ItemBarangUpdate, db: Session = Depends(get_db)):
    """
    Memperbarui detail produk berdasarkan ID (UUID).
    """
    db_product = db.query(models.ItemBarang).filter(models.ItemBarang.item_id == item_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Update atribut produk dari data yang diterima
    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.add(db_product) # Atau db.merge(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# --- Endpoint untuk Menghapus Produk ---
@app.delete("/products/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(item_id: str, db: Session = Depends(get_db)):
    """
    Menghapus produk dari database berdasarkan ID (UUID).
    """
    db_product = db.query(models.ItemBarang).filter(models.ItemBarang.item_id == item_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return

# --- Endpoint Utama ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to Rainshop API with SQLAlchemy!"}