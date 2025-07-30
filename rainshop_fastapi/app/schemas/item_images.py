from pydantic import BaseModel
from typing import Optional


class ItemImageBase(BaseModel):
    item_id: str
    image_path: str
    faiss_index: int = None

class ItemImageId(BaseModel):
    image_id: str

class ItemImageUpdate(BaseModel):
    image: str
    
class ItemImageForm(BaseModel):
    item_id: str
    image: str
    image_id: Optional[str] = None

class ItemImageCreate(ItemImageBase):
    image_id: Optional[str] = None



class ItemImageOut(ItemImageBase):
    image_id: str

    model_config = {
        "from_attributes": True
    }