from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils.print_helper import print_serial
# from app.utils.print_helper import print_serial, print_blutooth

router = APIRouter()

class PrintData(BaseModel):
    text: str

class PrintItem(BaseModel): #printer
    name: str
    qty: int
    price: int

class PrintRequest(BaseModel):
    bt_address: str
    items: List[PrintItem]

# @router.post("/print")
# def print(data: PrintData):
#     result = print_blutooth(data.text)
#     return result

@router.post("/print-struk")
async def print_struk(data: PrintRequest):
    total = sum([item.qty * item.price for item in data.items])
    result = print_serial(data.bt_address, data.items, total)
    return result
