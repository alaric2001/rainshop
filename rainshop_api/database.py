# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from dotenv import load_dotenv # Import load_dotenv

# from dotenv import load_dotenv
import os

# Muat variabel lingkungan file .env
# load_dotenv()
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# --- Konfigurasi Database dari Variabel Lingkungan ---
# Mengambil nilai dari .env atau menggunakan default jika tidak ditemukan
DB_HOST = os.getenv('DB_HOST', "localhost")
DB_PORT = os.getenv("DB_PORT", "3306") # Default MySQL port
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "rainshop")

# --- Print untuk Logging ---
print(f"DB_HOST: {DB_HOST}")
# print(os.getenv("DB_PORT","--"))
print(f"DB_PORT: {DB_PORT}")
print(f"DB_USER: {DB_USER}")
# Hati-hati saat logging password di lingkungan produksi!
# Untuk debugging lokal, ini mungkin OK, tapi sebaiknya hindari di produksi.
print(f"DB_PASSWORD: {'*' * len(DB_PASSWORD) if DB_PASSWORD else '[empty]'}")
print(f"DB_NAME: {DB_NAME}")

# --- Membuat URL Koneksi SQLAlchemy ---
# Format: mysql+pymysql://user:password@host:port/dbname
# Perhatikan bahwa password kosong tidak perlu ada di URL, kecuali jika ada karakter khusus.
# Untuk password kosong, cukup "user:@"
if DB_PASSWORD:
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
else:
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# --- Buat SQLAlchemy Engine ---
# engine adalah inti dari SQLAlchemy, ia mengelola koneksi ke database.
# pool_pre_ping=True membantu menjaga koneksi tetap hidup dan memeriksa validitasnya.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# --- Buat SessionLocal class ---
# Setiap instance SessionLocal akan menjadi session database.
# autocommit=False: Anda harus memanggil session.commit() secara eksplisit untuk menyimpan perubahan.
# autoflush=False: Tidak akan secara otomatis mem-flush data yang tertunda ke DB sampai commit.
# bind=engine: Mengikat session ke engine database yang telah kita buat.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base class untuk model deklaratif ---
# Ini adalah kelas dasar yang akan diwarisi oleh semua model ORM Anda (misalnya ItemBarang).
# Base ini akan digunakan oleh SQLAlchemy untuk memetakan kelas Python ke tabel database.
Base = declarative_base()

# --- Dependency untuk mendapatkan sesi database per request ---
# Fungsi ini akan digunakan oleh FastAPI untuk menyediakan sesi database ke endpoint.
# Ini memastikan bahwa setiap request mendapatkan sesi database-nya sendiri
# dan sesi tersebut ditutup dengan benar setelah request selesai (baik berhasil atau gagal).
def get_db():
    db = SessionLocal() # Buat sesi baru
    try:
        yield db # Berikan sesi ke endpoint FastAPI
    finally:
        db.close() # Pastikan sesi ditutup setelah selesai digunakan
