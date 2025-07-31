from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class SalesHeaderBase(BaseModel):
    sales_time: Optional[datetime] = None
    sales_no: Optional[str] = None
    sales_total: Optional[float] = None
    sales_paym: Optional[str] = "TUNAI"
    totalitem: Optional[str] = None

class SalesLineBase(BaseModel):
    sales_line_id: str
    sales_id: str
    item_id: str
    item_price: Optional[float] = None
    qty: int
    subtotal: Optional[float] = None

class VwSalesLineBase(BaseModel):
    item_id: str
    item_price: Optional[float] = None
    qty: int
    subtotal: Optional[float] = None
    item_name: str
    
class VwSalesLine(VwSalesLineBase):
    sales_line_id: str
    sales_id: str
    item_id: str
    item_price: Optional[float] = None
    qty: int
    subtotal: Optional[float] = None
    item_name: str
    item_price_skrg: Optional[float] = None
    item_stock: Optional[int] = None
    isactive: Optional[bool] = None
    image_id: Optional[str] = None  
      

class SalesHeaderCreate(SalesHeaderBase):
    sales_id: Optional[str] = None

class SalesLineCreate(SalesHeaderBase):
    sales_id: Optional[str] = None
    sales_line_id: Optional[str] = None
    item_stock: Optional[int] = None
    isactive: Optional[bool] = None
    image_id: Optional[str] = None  

class SalesForm(SalesHeaderBase):
    sales_id: Optional[str] = None
    lines: List[VwSalesLine] = []  


class SalesHeaderOut(SalesHeaderBase):
    sales_id: str
    lines: List[VwSalesLine] = []  # Gunakan schema output untuk images
    
    model_config = ConfigDict(
        from_attributes=True,  # Setara dengan orm_mode di Pydantic v1
    )