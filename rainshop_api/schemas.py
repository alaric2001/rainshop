# schemas.py (Contoh penyesuaian untuk DECIMAL)
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal # Impor Decimal

class ItemBarangCreate(BaseModel):
    item_name: str = Field(..., example="Kemeja Flanel")
    item_price: Decimal = Field(..., example=Decimal("150000.00")) # Gunakan Decimal
    isactive: int = Field(1, example=1, description="0 for inactive, 1 for active")

class ItemBarangUpdate(BaseModel):
    item_name: Optional[str] = Field(None, example="Kemeja Flanel Terbaru")
    item_price: Optional[Decimal] = Field(None, example=Decimal("160000.00")) # Gunakan Decimal
    isactive: Optional[int] = Field(None, example=0)

class ItemBarang(BaseModel):
    item_id: str
    item_name: str
    item_price: Decimal # Gunakan Decimal
    isactive: int

    class Config:
        from_attributes = True