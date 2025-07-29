from fastapi import APIRouter
from pydantic import BaseModel
from app.printers.print_utils import print_receipt

router = APIRouter()

class PrintData(BaseModel):
    text: str

@router.post("/print")
def print_to_bluetooth(data: PrintData):
    result = print_receipt(data.text)
    return result
