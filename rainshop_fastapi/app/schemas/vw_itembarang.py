from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

class VwItemBarangOut(BaseModel):
    item_id: str
    item_name: str
    item_price: float
    item_stock: int
    isactive: Optional[bool] = True
    image_id: Optional[str] = None
    image1: Optional[str] = None
    image2: Optional[str] = None
    image3: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,  # Setara dengan orm_mode di Pydantic v1
    )