from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from app.database import engine

# Gunakan Base yang sama dengan model lain (pastikan import dari modul yang sama)
from app.database import Base

class VwItemBarang(Base):
    __tablename__ = "vw_itembarang"
    __table_args__ = {'autoload_with': engine}  # jika kamu pakai engine + reflect
    __mapper_args__ = {
        "primary_key": ["item_id", "faiss_index"]  # karena view tidak punya PK, kamu harus tentukan manual
    }

    item_id = Column(String(36))
    item_name = Column(String(100))
    item_price = Column(Float)
    item_stock = Column(Integer)
    isactive = Column(Boolean)
    faiss_index = Column(Integer)
    image_path = Column(String(400))
    image_id = Column(String(36))

    # def to_dict(self):
    #     return {
    #         "item_id": self.item_id,
    #         "item_name": self.item_name,
    #         "item_price": self.item_price,
    #         "item_stock": self.item_stock,
    #         "isactive": self.isactive
    #         # tambahkan field lain sesuai kebutuhan
    #     }
