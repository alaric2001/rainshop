import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ItemImage(Base):
    __tablename__ = "item_images"

    image_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("itembarang.item_id"), nullable=False)
    image_path = Column(String(400), nullable=False)
    faiss_index = Column(Integer, unique=True, nullable=False)
    modified = Column(DateTime, nullable=True)

    item = relationship("ItemBarang", back_populates="images")
