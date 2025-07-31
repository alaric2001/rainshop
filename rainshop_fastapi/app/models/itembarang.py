from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class ItemBarang(Base):
    __tablename__ = "itembarang"

    item_id = Column(String(36), primary_key=True, index=True)
    item_name = Column(String(200), nullable=False)
    item_price = Column(Float, nullable=True)
    item_stock = Column(Integer, default=0)
    isactive = Column(Boolean, default=True)
    image_id = Column(String(36), nullable=True)

    images = relationship("ItemImage", back_populates="item", cascade="all, delete-orphan")
