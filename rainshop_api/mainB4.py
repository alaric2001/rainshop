# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import pymysql.cursors
from typing import List, Optional
import uuid

app = FastAPI()

# --- Konfigurasi Database ---
# Anda bisa menyimpan ini di file .env untuk keamanan (misalnya dengan python-dotenv)
# Tapi untuk contoh ini, kita hardcode dulu
DB_CONFIG = {
    "host": "127.0.0.1",   # Gunakan 127.0.0.1 atau localhost, diikuti dengan port
    "port": 7000,    
    "user": "root",       # Ganti dengan username MySQL Anda
    "password": "", # Ganti dengan password MySQL Anda
    "db": "rainshop",     # Nama database Anda
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor # Mengembalikan hasil sebagai dictionary
}

# --- Model Pydantic untuk Data Produk ---
class Product(BaseModel):
    item_id: Optional[str] = None # ID bisa opsional untuk POST (akan di-generate DB)
    item_name: str
    item_price: float
    isactive: int

# --- Dependency untuk Mendapatkan Koneksi Database ---
async def get_db():
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection # Mengembalikan koneksi ke endpoint
    finally:
        if connection:
            connection.close() # Pastikan koneksi ditutup setelah request selesai

# --- Endpoint untuk Menguji Koneksi (Opsional) ---
@app.get("/db-status")
async def get_db_status(db_conn: pymysql.connections.Connection = Depends(get_db)):
    """
    Endpoint untuk memeriksa status koneksi database.
    """
    try:
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                return {"status": "Database connection successful", "test_result": result}
            return {"status": "Database connection failed, no result from test query"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {e}"
        )

# --- Endpoint untuk Membuat Produk Baru ---
@app.post("/products/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product, db_conn: pymysql.connections.Connection = Depends(get_db)):
    """
    Menambahkan produk baru ke database.
    """
    try:
        with db_conn.cursor() as cursor:
            if product.item_id is None:
                product.item_id=str(uuid.uuid4())
                sql = "INSERT INTO itembarang (item_id, item_name, item_price, isactive) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (product.item_id, product.item_name, product.item_price, 1))
            else:
                sql = "UPDATE itembarang set item_name=%s, item_price=%s, isactive=%s WHERE item_id=%s"
                cursor.execute(sql, (product.item_name, product.item_price, product.isactive,  product.item_id))
            
            db_conn.commit() # Simpan perubahan

        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {e}"
        )

# --- Endpoint untuk Mendapatkan Semua Produk ---
@app.get("/products/", response_model=List[Product])
async def get_all_products(db_conn: pymysql.connections.Connection = Depends(get_db)):
    """
    Mendapatkan daftar semua produk dari database.
    """
    try:
        with db_conn.cursor() as cursor:
            sql = "SELECT item_id, item_name, item_price, isactive FROM itembarang"
            cursor.execute(sql)
            products = cursor.fetchall() # Ambil semua baris hasil
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve products: {e}"
        )

# --- Endpoint untuk Mendapatkan Produk Berdasarkan ID ---
@app.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: str, db_conn: pymysql.connections.Connection = Depends(get_db)):
    """
    Mendapatkan detail produk berdasarkan ID.
    """
    try:
        with db_conn.cursor() as cursor:
            sql = "SELECT item_id, item_name, item_price, isactive FROM itembarang WHERE item_id = %s"
            cursor.execute(sql, (product_id,))
            product = cursor.fetchone() # Ambil satu baris hasil
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {product_id} not found"
                )
        return product
    except Exception as e:
        if isinstance(e, HTTPException): # Jika error sudah HTTPException dari atas
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve product: {e}"
        )

# --- Endpoint Utama ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to Rainshop API!"}