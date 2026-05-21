# config.py
import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
parent_dir = dirname(dirname(__file__))
load_dotenv(dotenv_path)

# Optional: akses langsung variabel
DB_HOST = os.getenv('DB_HOST', "localhost")
DB_PORT = os.getenv("DB_PORT", "3306") # Default MySQL port
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "rainshop")
PRINTER_LIBUSB_PATH = join(
    parent_dir,
    "libusb-1.0.29", "VS2022", "MS64", "dll", "libusb-1.0.dll"
)