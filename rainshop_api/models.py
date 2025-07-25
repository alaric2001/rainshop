# models.py
from sqlalchemy import Column, String, DECIMAL, Integer
from sqlalchemy.dialects.mysql import TINYINT # Penting untuk tipe data tinyint
from .database import Base # Asumsi Base diimpor dari database.py

class ItemBarang(Base):
    __tablename__ = "itembarang" # Nama tabel di database Anda

    item_id = Column(String(50), primary_key=True, index=True)
    item_name = Column(String(200), nullable=False)
    item_price = Column(DECIMAL(29, 10), default=0.00) # Menggunakan DECIMAL untuk presisi
    isactive = Column(TINYINT(1), default=1) # tinyint(1) di MySQL

    def __repr__(self):
        return f"<ItemBarang(item_id='{self.item_id}', item_name='{self.item_name}')>"

