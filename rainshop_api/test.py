from dotenv import load_dotenv, find_dotenv, dotenv_values
import os

# Muat variabel lingkungan file .env
load_dotenv()

print(os.getenv('DB_HOST'))

print(dotenv_values('.env'))