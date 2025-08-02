from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Generic, TypeVar
from app.schemas.item_images import ItemImageOut  # Pastikan ini mengimport schema output

T = TypeVar('T')

class ItemBarangBase(BaseModel):
    item_name: str
    item_price: Optional[float] = None
    item_stock: Optional[int] = 0
    isactive: Optional[bool] = True
    image_id: Optional[str] = None

class ImageSearchRequest(BaseModel):
    image: str

class ItemBarangCreate(ItemBarangBase):
    item_id: Optional[str] = None
    image: str  # Untuk upload base64
    image2: Optional[str] = None
    image3: Optional[str] = None

class ItemBarangUpdate(ItemBarangBase):
    item_id: str

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    limit: int

# Schema yang sudah ada (ItemBarangOut) tetap dipertahankan
class ItemBarangOut(BaseModel):
    id: int
    item_name: str
    # ... field lainnya

class ItemBarangOut(ItemBarangBase):
    item_id: str
    images: List[ItemImageOut] = []  # Gunakan schema output untuk images
    
    model_config = ConfigDict(
        from_attributes=True,  # Setara dengan orm_mode di Pydantic v1
    )