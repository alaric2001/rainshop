from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.schemas.item_images import ItemImageOut  # Pastikan ini mengimport schema output

class ItemBarangBase(BaseModel):
    item_name: str
    item_price: Optional[float] = None
    item_stock: Optional[int] = 0
    isactive: Optional[bool] = True

class ImageSearchRequest(BaseModel):
    image: str

class ItemBarangCreate(ItemBarangBase):
    item_id: Optional[str] = None
    image: str  # Untuk upload base64
    image2: Optional[str] = None
    image3: Optional[str] = None

class ItemBarangUpdate(ItemBarangBase):
    item_id: str

class ItemBarangOut(ItemBarangBase):
    item_id: str
    images: List[ItemImageOut] = []  # Gunakan schema output untuk images
    
    model_config = ConfigDict(
        from_attributes=True,  # Setara dengan orm_mode di Pydantic v1
    )